import json
from PySide6.QtCore import QObject, Signal, QTimer, Slot


class PreactBridge(QObject):
  # Define a signal that JavaScript can listen to
  flight = Signal(str)
  config = Signal(str)
  status = Signal(dict)

  def __init__(self, parent, logger, flight_manager, app_manager, config_manager):
    super().__init__()
    self.parent = parent
    self.logger = logger
    self.flight_manager = flight_manager
    self.app_manager = app_manager
    self.config_manager = config_manager

    # Timer to trigger every 'get_new_flight_interval'
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.send_flight)
    self.timer.start(int(self.config_manager.get_config_value('app', 'get_new_flight_interval')) * 1000)

  def send_flight(self, hex_code: str = None):
    # Broadcast flight data to the frontend
    flight_data = self.flight_manager.get_flight_data(hex_code=hex_code)
    if flight_data is None:
      return
    self.logger.info(f"Callsign: {flight_data['toDisplay']['flight']['callsign']}")
    self.flight.emit(json.dumps(flight_data))

  def send_status(self, status: str, _type: str, message: str):
    self.status.emit({"status": status, "type": _type, "message": message})

  @Slot(result=str)
  def fetch_config(self):
    return json.dumps(self.config_manager.get_config())

  @Slot(str)
  def set_flight(self, hex_code: str):
    self.logger.info(f"New flight selected from frontend: {hex_code}")
    self.send_flight(hex_code)
