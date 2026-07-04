import time
from typing import Any
from PySide6.QtCore import Signal, Slot, QTimer
from classes import DisplayQueue, FlightData
from managers import Mgr
from utilities.flight_lookups import lookup_reg_from_hex, lookup_detail

DEFAULT_GET_FLIGHT_INTERVAL = 10


class DataMgr(Mgr):
  timer: QTimer
  cad: QTimer
  gf: QTimer
  gftd: QTimer
  gfl: QTimer

  send_flight_list = Signal(list)
  send_display_flight = Signal(dict)
  send_darkmode = Signal(bool)

  def __init__(self, logger, config):
    super().__init__(base_path="", logger=logger, name='BRIDGE', config=config)
    self.logger = logger
    self.config = config
    self.channel = None
    self.preact_connected = False

    self.flight_data: dict[str, FlightData] = {}
    self.display_queue = DisplayQueue()

  def activate(self):
    self.cad = QTimer()
    self.cad.timeout.connect(self.clean_adsb_data)
    self.cad.start(self.config.app.clean_interval * 1000)

    self.gf = QTimer()
    self.gf.timeout.connect(self.get_flight)
    self.gf.start(self.config.app.airplanes_live_reg_interval * 1000)

    self.gftd = QTimer()
    self.gftd.timeout.connect(self.get_flight_to_display)
    self.gftd.start(self.config.app.display_new_flight_interval * 1000)

    self.gfl = QTimer()
    self.gfl.timeout.connect(self.get_flight_list)
    self.gfl.start(self.config.app.update_flight_list * 1000)

    # self.timer.singleShot(self.config.app.clean_interval * 1000, self.clean_adsb_data)
    # self.timer.singleShot(self.config.app.airplanes_live_reg_interval * 1000, self.get_flight)
    # self.timer.singleShot(self.config.app.display_new_flight_interval * 1000, self.get_flight_to_display)
    # self.timer.singleShot(self.config.app.update_flight_list * 1000, self.get_flight_list)

  ########################################################
  # ADSB data reducer
  ########################################################
  @Slot(dict)
  def receive_adsb_data(self, data: dict[str, Any]):
    for hex_code, adsb in data.items():
      fd = self.flight_data.get(hex_code, None)
      if fd is None:
        self.flight_data.setdefault(hex_code, FlightData(hex_code=hex_code, adsb=adsb))
      else:
        fd.adsb.append(adsb)

  ########################################################
  # ADSB cleaning schedule
  ########################################################
  def clean_adsb_data(self):
    has_stale_age_seconds = self.config.app.has_stale_age_seconds
    now = time.time()
    for hex_key in list(self.flight_data.keys()):
      fd = self.flight_data[hex_key]
      last_idx = len(fd.adsb) - 1
      last_adsb = fd.adsb[last_idx]
      is_stale = now - last_adsb['time'] > has_stale_age_seconds
      if is_stale:
        self.flight_data.pop(hex_key, None)
        self.display_queue.remove(hex_key)

    self.status_counts()
    # self.timer.singleShot(self.config.app.clean_interval * 1000, self.clean_adsb_data)

  ########################################################
  # Get flight information from the hex code
  ########################################################
  def get_flight(self):
    # Get the next flight that has no registration or details
    hex_code, val = next(((k, v) for k, v in self.flight_data.items() if v.reg == '' and not v.ignore), (None, None))

    # Find the registration from the ICAO code
    # noinspection PyBroadException
    try:
      val.reg = lookup_reg_from_hex(hex_code=hex_code)
      fr24_detail = lookup_detail(reg=val.reg)
      if fr24_detail is not None:
        val.set_detail(fr24_detail)
        self.display_queue.add(hex_code)

    except Exception as e:
      if val is not None:
        val.ignore = True

    # self.timer.singleShot(self.config.app.airplanes_live_reg_interval * 1000, self.get_flight)

  ########################################################
  # Assemble the flights and send to Preact
  ########################################################
  def get_flight_list(self):
    flight_list = [
      val for val in self.flight_data.values()
      if val.fr24_detail is not None and val.ui_static_detail is not None and val.list_static_detail is not None
    ]

    flight_list = list(map(lambda x: x.package_for_flight_list(), flight_list))
    sorted_flight_list = sorted(flight_list, key=lambda x: x.get('callsign', ''))
    self.send_flight_list.emit(sorted_flight_list)
    # self.timer.singleShot(self.config.app.update_flight_list * 1000, self.get_flight_list)

  ########################################################
  # Pick flight detail to send to Preact
  ########################################################
  def get_flight_to_display(self):
    hex_code = self.display_queue.get_display_hex()
    if hex_code is not None:
      flight_data = self.flight_data[hex_code].package_for_flight_data()
      self.send_display_flight.emit(flight_data)
    # self.timer.singleShot(self.config.app.display_new_flight_interval * 1000, self.get_flight_to_display)

  # def package_flight_data(self, flight_detail: Any) -> dict[str, Any]:
  #   fr24_detail = flight_detail.detail
  #   adsbs = flight_detail.adsb
  #   if len(adsbs) == 0:
  #     squawk = ''
  #     lat = ''
  #     lon = ''
  #     lat_dir = '',
  #     lon_dir = '',
  #     observed = '0m 0s'
  #   else:
  #     last_adsb = adsbs[-1]
  #     first_adsb = adsbs[0]
  #     squawk = last_adsb.get('squawk', None)
  #     lat, lat_dir = decode_position(adsbs, 'lat')
  #     lon, lon_dir = decode_position(adsbs, 'lon')
  #     observed = sec_to_hhmmss(last_adsb.get('time', 0) - first_adsb.get('time', 0))
  #
  #   alt_value, alt_arrow, alt_class = get_value_arrow_class(adsbs, 'alt_baro', 'ud')
  #   gs_value, gs_arrow, gs_class = get_value_arrow_class(adsbs, 'gs', 'lr')
  #   hdg_value, hdg_arrow, hdg_class = get_value_arrow_class(adsbs, 'heading', 'lr')
  #
  #   hex_code = glom(fr24_detail, "aircraft.hex", default="---")
  #   registration = glom(fr24_detail, 'aircraft.registration', default="---")
  #   aircraft_type = glom(fr24_detail, 'aircraft.model.text', default="---")
  #   callsign = glom(fr24_detail, 'identification.callsign', default="Unknown")
  #   callsign_str = f"{callsign[:3]}{callsign[3:]}"
  #   airline_icao = glom(fr24_detail, 'airline.code.icao', default="UNK")
  #   aircraft_code = glom(fr24_detail, 'aircraft.model.code', default="")
  #   aircraft_country = glom(fr24_detail, 'aircraft.country.alpha2', default="ZZ")
  #   origin_iata = glom(fr24_detail, 'airport.origin.code.iata', default="---")
  #   origin_city = glom(fr24_detail, 'airport.origin.position.region.city', default="---")
  #   destination_iata = glom(fr24_detail, 'airport.destination.code.iata', default="---")
  #   destination_city = glom(fr24_detail, 'airport.destination.position.region.city', default="---")
  #
  #   scheduled_dep = glom(fr24_detail, 'time.scheduled.departure', default=None)
  #   scheduled_arr = glom(fr24_detail, 'time.scheduled.arrival', default=None)
  #   actual_dep = glom(fr24_detail, 'time.real.departure', default=None)
  #   est_arr = glom(fr24_detail, 'time.estimated.arrival', default=None)
  #
  #   # tz is "America/New_York"
  #   dep_tz = glom(fr24_detail, 'airport.origin.timezone.name', default=None)
  #   arr_tz = glom(fr24_detail, 'airport.destination.timezone.name', default=None)
  #
  #   # tz_abbr is "EDT"
  #   dep_tz_abbr = glom(fr24_detail, 'airport.origin.timezone.abbr', default="")
  #   arr_tz_abbr = glom(fr24_detail, 'airport.destination.timezone.abbr', default="")
  #
  #   scheduled_dep_str = format_time(scheduled_dep, dep_tz, dep_tz_abbr) if scheduled_dep is not None else "---"
  #   scheduled_arr_str = format_time(scheduled_arr, arr_tz, arr_tz_abbr) if scheduled_arr is not None else "---"
  #   actual_dep_str = format_time(actual_dep, dep_tz, dep_tz_abbr) if actual_dep != 0 else "---"
  #   est_arr_str = format_time(est_arr, arr_tz, arr_tz_abbr) if est_arr != 0 else "---"
  #
  #   if (scheduled_dep is not None and scheduled_arr is not None) and (actual_dep is not None and est_arr is not None):
  #     flight_time = scheduled_arr - scheduled_dep
  #     actual_time = est_arr - actual_dep
  #     dep_late = actual_dep - scheduled_dep
  #     arr_late = est_arr - scheduled_arr
  #     flight_time_str = sec_to_hhmmss(flight_time) if scheduled_arr != 0 and scheduled_dep != 0 else ""
  #     actual_time_str = sec_to_hhmmss(actual_time) if est_arr != 0 and actual_dep != 0 else ""
  #     actual_time_late = has_late(flight_time, actual_time)
  #     dep_is_late = has_late(scheduled_dep, actual_dep)
  #     arr_is_late = has_late(scheduled_arr, est_arr)
  #     flight_time_late = has_late(
  #       flight_time,
  #       actual_time
  #     )
  #     dep_lateness = scheduled_dep - actual_dep
  #     arr_lateness = scheduled_arr - est_arr
  #     dep_lateness_str = sec_to_hhmmss(dep_lateness)
  #     arr_lateness_str = sec_to_hhmmss(arr_lateness)
  #     dep_lateness_class = 'late' if dep_lateness < 0 else ''
  #     arr_lateness_class = 'late' if arr_lateness < 0 else ''
  #     origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
  #     origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
  #     destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
  #     destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
  #   else:
  #     flight_time_str = "---"
  #     actual_time_str = "---"
  #     dep_late = 0
  #     arr_late = 0
  #     actual_time_late = False
  #     dep_is_late = False
  #     arr_is_late = False
  #     flight_time_late = '---'
  #     dep_lateness_str = "---"
  #     arr_lateness_str = "---"
  #     dep_lateness_class = ''
  #     arr_lateness_class = ''
  #     origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
  #     origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
  #     destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
  #     destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
  #
  #   return {
  #     "hex_code": hex_code,
  #     "registration": registration,
  #     "squawk": squawk,
  #     "aircraft_type": aircraft_type,
  #     "callsign": callsign_str,
  #     "airline_icao": airline_icao,
  #     "aircraft_code": aircraft_code,
  #     "country": aircraft_country,
  #     "origin_iata": origin_iata,
  #     "origin_city": origin_city,
  #     'lat': lat,
  #     'lon': lon,
  #     'lat_dir': lat_dir,
  #     'lon_dir': lon_dir,
  #
  #     "alt_value": alt_value,
  #     "alt_arrow": alt_arrow,
  #     "alt_class": alt_class,
  #     "gs_value": gs_value,
  #     "gs_arrow": gs_arrow,
  #     "gs_class": gs_class,
  #     "hdg_value": hdg_value,
  #     "hdg_arrow": hdg_arrow,
  #     "hdg_class": hdg_class,
  #
  #     "destination_iata": destination_iata,
  #     "destination_city": destination_city,
  #     "scheduled_dep": scheduled_dep_str,
  #     "scheduled_arr": scheduled_arr_str,
  #     "actual_dep": actual_dep_str,
  #     "est_arr": est_arr_str,
  #     "flight_time": flight_time_str,
  #     "actual_time": actual_time_str,
  #     "dep_late_str": sec_to_hhmmss(abs(dep_late)) if dep_late > 0 else "---",
  #     "arr_late_str": sec_to_hhmmss(abs(arr_late)) if arr_late > 0 else "---",
  #     "flight_time_late": flight_time_late,
  #     "dep_is_late": dep_is_late,
  #     "arr_is_late": arr_is_late,
  #     "actual_time_late": actual_time_late,
  #     "dep_lateness_str": dep_lateness_str,
  #     "arr_lateness_str": arr_lateness_str,
  #     "dep_lateness_class": dep_lateness_class,
  #     "arr_lateness_class": arr_lateness_class,
  #     "observed": observed,
  #   }

  ########################################################
  # Logging information
  ########################################################
  def status_counts(self):
    with_reg = sum(1 for obj in self.flight_data.values() if obj.reg is not None)
    without_reg = sum(1 for obj in self.flight_data.values() if obj.reg is None)
    # with_detail = sum(1 for obj in self.flight_data.values() if obj.detail is not None)
    ignored = sum(1 for obj in self.flight_data.values() if obj.ignore)
    length = len(self.flight_data)
    self.logger.info(f"DataBridgeMgrStatus: {length} | {with_reg} | {without_reg} | {ignored}")

  # # Send values to Preact
  # send_config = Signal(dict)
  # send_darkmode = Signal(bool)
  # send_flight_data = Signal(dict)  # Flight data to preact
  # send_flight_list = Signal(dict)
  #
  # # Send Preact ready to other managers
  # send_preact_ready = Signal()
  #
  # def __init__(self, logger, config):
  #   super().__init__(base_path="", logger=logger, name='BRIDGE', config=config)
  #   self.logger = logger
  #   self.config = config
  #   self.channel = None
  #   self.preact_connected = False
  #   self.timer = QTimer()
  #
  # def activate(self):
  #   if self.preact_connected:
  #     self._send_config_to_preact()
  #   else:
  #     self.logger.info("DataBridgeMgr received config before Preact connected; config cached")
  #   self.logger.info("ACTIVATE")
  #   self.timer.singleShot(self.config.app.get_new_flight_interval * 1000, self.get_new_flight)
  #
  # ########################################################
  # # Error in manager(s)
  # ########################################################
  # @Slot(str, str)
  # def receive_error(self, error_type: str, error_msg: str):
  #   self.logger.error(f"DataBridgeMgr received error: {error_type}: {error_msg}")
  #
  # ########################################################
  # # Receive communication channel from the UI manager
  # ########################################################
  # @Slot(object)
  # def receive_channel(self, channel):
  #   self.channel = channel
  #

#
# @Slot(dict)
# def receive_flight_list(self, flight_list):
#   serialized_flights = to_plain_dict(flight_list)
#   # self.logger.info(f"DataBridgeMgr: received flight list: {serialized_flights}")
#   self.send_flight_list.emit(serialized_flights)
#
# @Slot(dict)
# def receive_flight_info(self, flight_data):
#   serialized_flight_data = to_plain_dict(flight_data)
#   self.send_flight_data.emit(serialized_flight_data)
#
# ########################################################
# # Receive Preact ready signal from the Preact app
# ########################################################
# @Slot()
# def preact_ready(self):
#   if self.config is not None:
#     self.preact_connected = True
#     self._send_config_to_preact()  # Send config to Preact
#     self.send_preact_ready.emit()  # DO I NEED THIS???
#     self.logger.info("PreactConnected")
#   else:
#     self.logger.info("PreactConnectedNoConfig")
#
# def _send_config_to_preact(self):
#   self.logger.info("SendConfigToPreact")
#   serialized_config = to_plain_dict(self.config)
#   self.send_config.emit(serialized_config)
