from PySide6.QtCore import Signal, Slot, QTimer
from managers import Mgr
from utilities import to_plain_dict


class BridgeMgr(Mgr):
  timer: QTimer
  send_config = Signal(dict)
  send_darkmode = Signal(bool)
  send_flight_list = Signal(list)
  send_flight_data = Signal(dict)

  def __init__(self, logger, config):
    super().__init__(base_path="", logger=logger, name='BRIDGE', config=config)
    self.logger = logger
    self.config = config
    self.channel = None
    self.preact_connected = False

  def activate(self):
    if self.preact_connected:
      self.send_config_to_preact()
    else:
      self.logger.info("DataBridgeMgr received config before Preact connected; config cached")

  ########################################################
  # Receive Preact ready signal from the Preact app
  ########################################################
  @Slot()
  def preact_ready(self):
    if self.config is not None:
      self.preact_connected = True
      self.send_config_to_preact()  # Send config to Preact
      self.logger.info("PreactConnected")
    else:
      self.logger.info("PreactConnectedNoConfig")

  def send_config_to_preact(self):
    self.logger.info("SendConfigToPreact")
    serialized_config = to_plain_dict(self.config)
    self.send_config.emit(serialized_config)

  ########################################################
  # Receive data from Python managers...
  # ...then send the data on to Preact
  ########################################################
  @Slot(dict)
  def receive_flight_list(self, flight_list):
    if self.preact_connected:
      self.send_flight_list.emit(flight_list)

  @Slot(bool)
  def receive_darkmode(self, darkmode: bool):
    if self.preact_connected:
      self.send_darkmode.emit(darkmode)

  @Slot(dict)
  def receive_display_flight(self, flight_data: dict):
    if self.preact_connected:
      self.send_flight_data.emit(flight_data)
