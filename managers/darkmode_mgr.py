import datetime
from PySide6.QtCore import QTimer, Signal, Slot
from suntime import Sun
from managers import Mgr


class DarkModeMgr(Mgr):
  darkmode = Signal(bool)

  def __init__(self, logger, base_path, config):
    super().__init__(logger=logger, config=config, base_path=base_path, name="DARKMODE")
    self.delay = self.config.app.get_dark_mode_interval * 1000
    self.config = config
    self.ready = False
    self.timer = None

  @Slot()
  def activate(self):
    self.timer = QTimer(self)
    self.timer.singleShot(self.delay, self.check_dark_mode)

  def check_dark_mode(self):
    self.logger.info(f"CheckDarkMode")
    sun = Sun(self.config.user.lat, self.config.user.lon)
    now = datetime.datetime.now()
    sunrise_utc = sun.get_sunrise_time(now)
    sunset_utc = sun.get_sunset_time(now)
    local_sunrise = sunrise_utc.astimezone()
    local_sunset = sunset_utc.astimezone()

    # --- FIX FOR SUNTIME BUG ---
    # If sunset is calculated as earlier than sunrise, it grabbed yesterday's data.
    # We shift it forward by 1 day to match the correct local "today".
    if local_sunset < local_sunrise:
      local_sunset += datetime.timedelta(days=1)

    now_aware = now.astimezone()
    if local_sunrise <= now_aware <= local_sunset:
      self.darkmode.emit(False)
      self.logger.info("check_dark_mode FALSE")
    else:
      self.darkmode.emit(True)
      self.logger.info("check_dark_mode TRUE")

    # Schedule the next check - get_dark_mode_interval is in minutes
    self.timer.singleShot(self.delay, self.check_dark_mode)
