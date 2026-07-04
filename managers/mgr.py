from PySide6.QtCore import QObject, Slot, Signal, QTimer

from config import Config


# from classes import Config


class Mgr(QObject):
  config: Config
  send_error = Signal(str, str)

  def __init__(self, logger, config, base_path="", name: str = "anonymous"):
    super().__init__()
    self.logger = logger
    self.base_path = base_path
    self.config = config
    self.name = name.upper()
    self.error = False
    self.error_msg = ""
    self.config_ready = False
    self.logger.info(f"{self.name}-INIT")

  def is_error(self):
    return self.error

  def get_error_msg(self):
    return self.error_msg

  def get_name(self):
    return self.name

  # @Slot(Config)
  # def receive_config(self, config: Config):
  #   if config is None:
  #     self.error = True
  #     self.error_msg = "ConfigError-NoConfig"
  #     return
  #   else:
  #     self.config = config
  #     self.config_ready = True
  #     self.activate()
