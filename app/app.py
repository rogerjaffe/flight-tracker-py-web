import os
import sys

# Forces Qt to use the Pi's GPU for rendering the WebEngine elements
os.environ["QT_XCB_GL_INTEGRATION"] = "xcb_egl"
os.environ["WEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu-vsync --shared-array-buffer"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["PYTHONUNBUFFERED"] = "1"

from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from typing import Optional
from classes import Worker, PreactBridge, ThreadedHTTPServer
from managers import ConfigManager, AppManager, FlightManager
from services import SvcGetFlights


class App():
  def __init__(self, base_path, logger, config_file='config.ini'):
    self.base_path = base_path
    self.logger = logger
    self.is_dev = os.environ.get('ENVIRONMENT', 'prod') == 'dev'
    self.APP_NAME = "Flight Tracker"
    self.data_push_timer = None
    self.port = 5173
    self.window: Optional[QWidget] = None

    # Add remote debugging for dev mode
    if self.is_dev:
      os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "9222"

    # If prod, start a simple http server to serve the UI
    # If dev then we're running a separate Vite dev server
    if not self.is_dev:
      self.http_server = ThreadedHTTPServer(directory_to_serve=os.path.join(base_path, 'preact/dist'))
      self.port = self.http_server.port
    self.logger.info(f"HTTP Server started on port {self.port}")

    # Application and QtSide6 definition
    self.application = QApplication(sys.argv)
    QCoreApplication.setApplicationName(self.APP_NAME)
    self.application.setApplicationDisplayName(self.APP_NAME)

    # Managers
    self.config_manager = ConfigManager(base_path=self.base_path, config_file=config_file)
    self.app_manager = AppManager(logger=self.logger, base_path=self.base_path, config_manager=self.config_manager)
    self.flight_manager = FlightManager(
      base_path=self.base_path,
      app_manager=self.app_manager,
      config_manager=self.config_manager)

    ##################################################################
    # Workers and threads, and processing queue
    ##################################################################
    self.workers = []

    # Start business logic
    self.start_business_logic(flight_manager=self.flight_manager)

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

    self.channel = QWebChannel(self.browser.page())
    self.preact_bridge = PreactBridge(
      parent=self.application,
      logger=self.logger,
      flight_manager=self.flight_manager,
      app_manager=self.app_manager,
      config_manager=self.config_manager)

    self.app_manager.set_browser(self.browser)
    self.app_manager.set_preact_bridge(self.preact_bridge)
    # self.app_manager.init_config()

    self.channel.registerObject('backend', self.preact_bridge)
    self.browser.page().setWebChannel(self.channel)

    # Callback for when the browser has finished loading
    self.browser.loadFinished.connect(self.on_browser_load_finished)
    browser_url = f"http://localhost:{self.http_server.port}" if not self.is_dev else "http://localhost:5173"
    self.browser.setUrl(browser_url)

    # Open the app window!
    if self.is_dev:
      self.window.show()
    else:
      self.window.showFullScreen()

    # Check all components are ready and error-free
    self.check_status()

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

  # Loads the QtSide6 UI file and returns the window object
  def load_ui(self):
    ui_file_name = self.config_manager.get_config_value('app', 'ui_file_name')

    # Keep the path as a standard string
    ui_file_path = os.path.join(self.base_path, 'app', ui_file_name)
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

  # Instantiates the services and starts the workers
  # executing the services
  def start_business_logic(self, flight_manager: FlightManager):
    svc_get_flights = SvcGetFlights(
      queue=flight_manager.queue,
      name='get_flights',
      lat=float(self.config_manager.get_config_value('user', 'home_lat')),
      lon=float(self.config_manager.get_config_value('user', 'home_lon')),
      radius=float(self.config_manager.get_config_value('user', 'home_radius')))
    flights_worker = Worker(
      delay=int(self.config_manager.get_config_value('get_flights', 'delay')),
      service=svc_get_flights,
      name='get_flights')
    self.workers.append(flights_worker)

  def check_status(self):
    self.logger.info("Checking status")
