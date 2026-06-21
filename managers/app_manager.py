import configparser
import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWebEngineCore import QWebEngineSettings
from suntime import Sun


class AppManager:
  def __init__(self, logger, base_path, config_manager):
    self.logger = logger
    self.base_path = base_path
    self.browser = None
    self.config_manager = config_manager

  # def get_config(self):
  #   return self.config
  #
  # def get_config_group(self, group_name: str):
  #   return dict(self.config[group_name])
  #
  # def get_config_value(self, group_name: str, key: str):
  #   return self.config[group_name][key]
  #
  def set_browser(self, browser):
    self.browser = browser
    QTimer.singleShot(int(self.config_manager.get_config_value('get_dark_mode', 'delay')) * 1000, self.check_dark_mode)

  def set_preact_bridge(self, preact_bridge):
    self.preact_bridge = preact_bridge
    QTimer.singleShot(int(self.config_manager.get_config_value('get_dark_mode', 'delay')) * 1000, self.check_dark_mode)

  def check_dark_mode(self):
    latitude = float(self.config_manager.get_config_value('user', "home_lat"))
    longitude = float(self.config_manager.get_config_value("user", "home_lon"))

    sun = Sun(latitude, longitude)

    # 1. Get current local time
    now = datetime.datetime.now()

    # 2. Get UTC times from suntime
    sunrise_utc = sun.get_sunrise_time(now)
    sunset_utc = sun.get_sunset_time(now)

    # 3. Convert both to your local timezone
    local_sunrise = sunrise_utc.astimezone()
    local_sunset = sunset_utc.astimezone()

    # --- FIX FOR SUNTIME BUG ---
    # If sunset is calculated as earlier than sunrise, it grabbed yesterday's data.
    # We shift it forward by 1 day to match the correct local "today".
    if local_sunset < local_sunrise:
      local_sunset += datetime.timedelta(days=1)

    # Ensure 'now' has timezone info to safely compare
    now_aware = now.astimezone()

    # 4. Determine day or night
    if local_sunrise <= now_aware <= local_sunset:
      self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, False)
    else:
      self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, True)

    QTimer.singleShot(int(self.config_manager.get_config_value('get_dark_mode', 'delay')) * 1000, self.check_dark_mode)
