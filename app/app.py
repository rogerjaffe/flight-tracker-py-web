import os

from managers.adsb_mgr import ADSBMgr
from managers.bridge_mgr import BridgeMgr
from managers.ui_mgr import UIMgr

# Forces Qt to use the Pi's GPU for rendering the WebEngine elements
os.environ["QT_XCB_GL_INTEGRATION"] = "xcb_egl"
os.environ["WEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu-vsync --shared-array-buffer"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["PYTHONUNBUFFERED"] = "1"

from PySide6.QtWidgets import QWidget
from typing import Optional, Any, Callable
from classes import MessageLogger
from managers import DarkModeMgr, DataMgr


class App():
  def __init__(self, base_path, logger, config):
    self.base_path = base_path
    self.config = config
    self.logger = logger
    self.is_dev = os.environ.get('ENVIRONMENT', 'prod') == 'dev'
    self.APP_NAME = "Flight Tracker"
    self.port = 5173
    self.window: Optional[QWidget] = None

    # Add remote debugging for dev mode
    if self.is_dev:
      os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "9222"

    self.message_logger = MessageLogger(logger=self.logger)

    self.data_mgr = DataMgr(logger=self.logger, config=self.config)
    self.adsb_mgrs = [
      ADSBMgr(logger=self.logger, config=self.config, adsb_server_config=adsb_server_config)
      for adsb_server_config in self.config.adsb_servers
    ]
    self.darkmode_mgr = DarkModeMgr(logger=self.logger, base_path=self.base_path, config=self.config)
    self.bridge_mgr = BridgeMgr(logger=self.logger, config=self.config)
    self.ui_mgr = UIMgr(
      logger=self.logger,
      base_path=self.base_path,
      app_name=self.APP_NAME,
      bridge_mgr=self.bridge_mgr,
      is_dev=self.is_dev, config=self.config)

    connection_list: list[tuple[str, str, Any, Callable[..., Any]]] = [
      ('ui', 'data', self.ui_mgr.send_ui_ready, self.data_mgr.activate),
      ('ui', 'bridge', self.ui_mgr.send_ui_ready, self.bridge_mgr.activate),
      ('ui', 'darkmode', self.ui_mgr.send_ui_ready, self.darkmode_mgr.activate),

      ('data', 'bridge', self.data_mgr.send_flight_list, self.bridge_mgr.receive_flight_list),
      ('data', 'bridge', self.data_mgr.send_display_flight, self.bridge_mgr.receive_display_flight),

      ('darkmode', 'bridge', self.darkmode_mgr.darkmode, self.bridge_mgr.receive_darkmode),
    ]
    for adsb_mgr in self.adsb_mgrs:
      # Connect ADSB managers to ui manager for activation
      connection_list.append(('ui', adsb_mgr.get_name(), self.ui_mgr.send_ui_ready, adsb_mgr.activate))
      # Connect ADSB managers to the data manager to process adsb data
      connection_list.append(
        (adsb_mgr.get_name(), 'data', adsb_mgr.send_adsb_data, self.data_mgr.receive_adsb_data))

    # Intercept the signals and log them
    for signal_name, slot_name, signal, slot in connection_list:
      self.message_logger.connect_and_log(signal=signal, slot=slot, signal_name=signal_name, slot_name=slot_name)

    self.ui_mgr.activate()
