import copy
import logging
import queue
import threading
import time
import re
from FlightRadarAPI import Flight
from glom import glom

from classes import DisplayQueue
from models import AppManager
from utilities import http_request


class FtFlight:
  def __init__(self, _hex: str, flight: Flight):
    self.flight = flight
    self.hex = _hex
    self.position = []
    self.add_position(flight)

  def add_position(self, flight):
    position = {"latitude": flight.latitude, "longitude": flight.longitude, "ground_speed": flight.ground_speed,
                "heading": flight.heading, "squawk": flight.squawk, "vertical_speed": flight.vertical_speed,
                "timestamp": time.time(), "altitude": flight.altitude}
    self.position.append(position)

  def add(self, flight: Flight):
    self.flight = flight
    self.add_position(flight)

  def to_dict(self):
    return {
      "hex": self.hex,
      "flight": vars(self.flight),
      "position": self.position,
    }


class FlightManager:
  def __init__(self, app_manager: AppManager, base_path: str, config_manager):
    self.app_manager = app_manager
    self.base_path = base_path
    self.config_manager = config_manager
    self.logger = logging.getLogger(__name__)
    self.ft_flights: dict[str, FtFlight] = {}
    self.display_queue = DisplayQueue()
    self.wait_cycles = 0

    self.state_lock = threading.Lock()
    self.queue = queue.Queue()

    # 1. Launch the continuous state manager as a daemon thread
    # (Daemon means it will close automatically when your main program shuts down)
    self.consumer = threading.Thread(target=self.queue_processor, daemon=True)
    self.consumer.start()

  def queue_processor(self):
    while True:
      try:
        # .get() BLOCKS here automatically if the queue is empty.
        # It does not spin or burn CPU cycles while waiting.
        task = self.queue.get(timeout=1.0)
      except queue.Empty:
        continue

      try:
        task_type = task.get("type")
        data = task.get("data")

        with self.state_lock:
          # Route to the correct write query based on the task type
          if task_type == "SHUTDOWN":
            break

          elif task_type == "ADD_FLIGHTS":
            self.add_flights(data)

          else:
            self.logger.error(f"Unknown queue task type: {task_type}")

      except Exception(BaseException):
        self.logger.exception(f"Error while processing queue task: {task}")

      finally:
        self.queue.task_done()
        self.logger.info(f"FtFlights size: {len(self.ft_flights)}")
        self.logger.info("====================================")

  def add_flights(self, data: list[Flight]):
    for flight in data:
      if flight.hex == '' or flight.hex is None:
        continue
      if flight.hex not in self.ft_flights:
        self.ft_flights[flight.hex] = FtFlight(flight.hex, flight)
      else:
        self.ft_flights[flight.hex].add(flight)

    # 2. DELETE keys from old_dict that do not exist in new_dict
    # We use list() to safely delete items while iterating
    hex_list = [item.hex for item in data]
    for hex_key in list(self.ft_flights.keys()):
      if hex_key not in hex_list:
        del self.ft_flights[hex_key]

  def filter_flights(self):
    clone = copy.deepcopy(self.ft_flights)
    if self.config_manager.get_config_value('app', 'airlines_only'):
      regex = re.compile(r'^[A-Z]{3}[0-9]{1,4}$')
      clone = {k: v for k, v in clone.items() if regex.match(v.flight.callsign)}

    if self.config_manager.get_config_value('app', 'has_position'):
      clone = {k: v for k, v in clone.items() if v.flight.latitude is not None and v.flight.longitude is not None}

    if not self.config_manager.get_config_value('app', 'on_ground'):
      clone = {k: v for k, v in clone.items() if v.flight.on_ground == 0}

    if self.config_manager.get_config_value('app', 'has_origin_destination'):
      clone = {k: v for k, v in clone.items() if
               v.flight.origin_airport_iata != '' and v.flight.destination_airport_iata != ''}

    return clone

  def get_flight_data(self, hex_code: str = None):
    if self.wait_cycles > 0 and hex_code is None:
      self.wait_cycles = self.wait_cycles - 1
      return None
    # Filter the flights based on config criteria
    # Lookup registration using URL above (find the field "type": "live" and the callsign matches the search key
    # Lookup flight details using the FR24 list.json URL:
    #  https://api.flightradar24.com/common/v1/flight/list.json?fetchBy=flight&page=1&limit=50&live=1&query=FX3619
    # Get ADSB data for the hex code
    # Pass all flight and adsb data to app
    if len(self.ft_flights) == 0:
      return {"flight_list": [], "flight": None}

    with self.state_lock:
      if len(self.ft_flights) == 0:
        self.display_queue.clear()
        return {"flight_list": {}, "flight": None}

      # Reconcile the new data set with the display queue,
      # adding the new hex codes to flights that don't already appear
      # and removing the hex codes from flights that are no
      # longer in the data set.
      clone = self.filter_flights()
      keys = list(clone.keys())
      self.display_queue.process_new_data(keys)
      if hex_code is None:
        key = self.display_queue.get_display_hex()
      else:
        key = hex_code
        self.wait_cycles = self.wait_cycles + 1
        self.display_queue.move_to_end(key)
      flight = clone[key]

      registration = flight.flight.registration
      url = (
        f"https://api.flightradar24.com/common/v1/flight/list.json?fetchBy=reg&page=1&limit=50&live=1&query="
        f"{registration}")
      detail = http_request(url, 'GET')
      data = glom(detail, 'result.response.data', default=[])
      match = next((x for x in data if glom(x, 'status.live', default=False)), None)

      return {
        "flightList": {hex_code: ft_flight.to_dict() for hex_code, ft_flight in clone.items()},
        "toDisplay": flight.to_dict(),
        "detail": match
      }
