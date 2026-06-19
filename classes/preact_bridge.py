import json
from PySide6.QtCore import QObject, Signal, QTimer, Slot


class PreactBridge(QObject):
  # Define a signal that JavaScript can listen to
  flight = Signal(str)
  config = Signal(str)

  def __init__(self, parent, logger, flight_manager, app_manager):
    super().__init__()
    self.parent = parent
    self.logger = logger
    self.flight_manager = flight_manager
    self.app_manager = app_manager

    # Timer to trigger every 'get_new_flight_interval'
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.send_flight)
    self.timer.start(int(self.app_manager.get_config_value('app', 'get_new_flight_interval')) * 1000)

  def send_config(self):
    # Broadcast config to the frontend
    self.config.emit('{"message": "config", "status": "ok"}')

  def send_flight(self):
    # Broadcast flight data to the frontend
    flight_data = self.flight_manager.get_flight_data()
    self.logger.info(f"Callsign: {flight_data['toDisplay']['flight']['callsign']}")
    self.flight.emit(json.dumps(flight_data))

  @Slot(result=str)
  def fetch_config(self):
    cfg = self.app_manager.config
    config_dict = {
      section: {k: v for k, v in cfg[section].items() if k not in cfg.defaults()}
      for section in cfg.sections()
    }
    return json.dumps(config_dict)
