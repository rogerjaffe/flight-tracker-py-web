import os
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt, Slot, Signal

from classes import ThreadedHTTPServer
from managers import Mgr

UI_FILE_NAME = 'flight-tracker.ui'


class UIMgr(Mgr):
  send_channel_to_bridge = Signal(object)
  send_ui_ready = Signal()

  def __init__(self, logger, base_path, bridge_mgr, app_name: str, is_dev: bool, config):
    super().__init__(base_path=base_path, logger=logger, name="UI", config=config)
    self.is_dev = is_dev
    self.ui_file_name = ""
    self.ui_file_name = UI_FILE_NAME
    self.app_name = app_name
    self.config = config
    self.application = None
    self.window = None
    self.browser = None
    self.channel = None
    self.http_server = None
    self.bridge_mgr = bridge_mgr
    self.port = 5173

  def activate(self):
    # Application and QtSide6 definition
    self.application = QApplication(sys.argv)
    QCoreApplication.setApplicationName(self.app_name)
    self.application.setApplicationDisplayName(self.app_name)

    # Load the Python UI configuration file
    self.window = self.load_ui()
    if not self.window:
      self.logger.error("UnableToLoadPythonUIError")
      return

    # Frameless window directive
    self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    if not self.is_dev:
      self.window.setWindowFlags(
        Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.CustomizeWindowHint
      )

    # Find the QWebEngineView widget in the UI
    self.browser = self.window.findChild(QWebEngineView, 'browser')
    if self.browser is None:
      self.logger.error("UnableToFindBrowserWidgetError")
      return

    # Set up a communication channel between the Python and TS code
    self.channel = QWebChannel(self.browser.page())
    self.channel.registerObject('backend', self.bridge_mgr)
    self.browser.page().setWebChannel(self.channel)

    profile = QWebEngineProfile.defaultProfile()
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)

    # Set up permissions for browser to load other files
    permission_attributes = [
      QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
      QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
      QWebEngineSettings.WebAttribute.JavascriptEnabled,
      QWebEngineSettings.WebAttribute.AllowRunningInsecureContent
    ]
    for attribute in permission_attributes:
      self.browser.settings().setAttribute(attribute, True)

    # If prod, start a simple http server to serve the UI
    # If dev then we're running a separate Vite dev server
    if not self.is_dev:
      self.http_server = ThreadedHTTPServer(directory_to_serve=os.path.join(self.base_path, 'preact/dist'))
      self.port = self.http_server.port
    self.logger.info(f"HTTP Server started on port {self.port}")

    # Callback for when the browser has finished loading
    self.browser.loadFinished.connect(self.on_browser_load_finished)
    browser_url = f"http://localhost:{self.http_server.port}" if not self.is_dev else "http://localhost:5173"
    self.browser.setUrl(browser_url)

    # Open the app window!
    if self.is_dev:
      self.window.show()
    else:
      self.window.showFullScreen()

    self.send_ui_ready.emit()
    sys.exit(self.application.exec())

  # Handles the browser load finished event
  def on_browser_load_finished(self, ok):
    if self.browser is None:
      self.logger.error('BrowserLoadError')
      return

    if not ok:
      self.logger.error("BrowserLoadFailed")
      return

    self.logger.info("BrowserLoadSuccessful")
    self.send_channel_to_bridge.emit(self.channel)

  # Loads the QtSide6 UI file and returns the window object
  def load_ui(self):
    # Keep the path as a standard string
    ui_file_path = os.path.join(self.base_path, 'app', self.ui_file_name)
    loader = QUiLoader()
    try:
      # Pass the string path directly; QUiLoader handles the IO internally
      window = loader.load(ui_file_path)
      if not window:
        self.logger.error('LoadUIError')
        return None
      return window
    except Exception as e:
      self.logger.error(f'OpenUIFileError: {e}')
      return None
