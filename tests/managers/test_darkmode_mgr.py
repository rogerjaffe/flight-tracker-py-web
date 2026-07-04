import pytest
import datetime
from unittest.mock import MagicMock
from PySide6.QtCore import QObject

from managers.darkmode_mgr import DarkModeMgr


class FakeMgr(QObject):
  """A clean PySide6 QObject to serve as a safe base class for testing."""

  def __init__(self, logger, base_path):
    super().__init__()
    self.logger = logger
    self.base_path = base_path


@pytest.fixture
def clean_darkmode_mgr(monkeypatch):
  """Safely constructs DarkModeMgr by substituting the parent class and mocking Sun/QTimer."""
  monkeypatch.setattr("managers.darkmode_mgr.Mgr", FakeMgr)

  mock_sun_instance = MagicMock()
  monkeypatch.setattr("managers.darkmode_mgr.Sun", lambda lat, lon: mock_sun_instance)

  mock_timer_single_shot = MagicMock()
  monkeypatch.setattr("managers.darkmode_mgr.QTimer.singleShot", mock_timer_single_shot)

  def _initializer():
    return DarkModeMgr(logger=MagicMock(), base_path="/fake/path")

  return {
    "initializer": _initializer,
    "sun_instance": mock_sun_instance,
    "timer": mock_timer_single_shot
  }


def test_set_config(clean_darkmode_mgr):
  """Verifies that setting configuration with a dictionary updates parameters and activates tracking."""
  ctx = clean_darkmode_mgr
  mgr = ctx["initializer"]()

  config_dict = {
    'user': {'home_lat': 32.7157, 'home_lon': -117.1611},
    'darkmode': {'poll_interval': 60}
  }

  mgr.set_config(config_dict)

  assert mgr.lat == 32.7157
  assert mgr.lon == -117.1611
  assert mgr.poll_interval == 60
  mgr.logger.info.assert_called_with("DarkModeMgr-set_config")
  ctx["timer"].assert_called_once_with(60000, mgr.check_dark_mode)


@pytest.mark.parametrize(
  "now_val, expected_darkmode", [
    (12, False),  # Midday (12) is between Sunrise (6) and Sunset (18) -> Daytime (False)
    (4, True),  # Early Morning (4) is before Sunrise (6) -> Nighttime (True)
    (23, True),  # Late Night (23) is after Sunset (18) -> Nighttime (True)
  ])
def test_check_dark_mode_evaluation(clean_darkmode_mgr, monkeypatch, now_val, expected_darkmode):
  """Verifies daytime vs nighttime calculations with regular sunrise and sunset timelines."""
  ctx = clean_darkmode_mgr
  mgr = ctx["initializer"]()

  config_dict = {
    'user': {'home_lat': 32.7, 'home_lon': -117.1},
    'darkmode': {'poll_interval': 30}
  }
  mgr.set_config(config_dict)
  ctx["timer"].reset_mock()

  # Generate specialized mock datetimes using integer abstractions for clean comparisons
  mock_now_aware = MagicMock()

  mock_now = MagicMock(spec=datetime.datetime)
  mock_now.astimezone.return_value = mock_now_aware

  mock_sunrise = MagicMock()
  mock_sunrise.astimezone.return_value = 6  # Fake Sunrise hour

  mock_sunset = MagicMock()
  mock_sunset.astimezone.return_value = 18  # Fake Sunset hour

  # Implement conditional comparison behaviors directly onto the mocks
  mock_sunset.__lt__ = lambda self, other: False  # Sunset is after sunrise
  mock_now_aware.__ge__ = lambda self, other: now_val >= other  # local_sunrise <= now_aware
  mock_now_aware.__le__ = lambda self, other: now_val <= other  # now_aware <= local_sunset

  ctx["sun_instance"].get_sunrise_time.return_value = mock_sunrise
  ctx["sun_instance"].get_sunset_time.return_value = mock_sunset

  # Create modular mock objects for datetime tracking instead of local syntax classes
  mock_datetime_class = MagicMock()
  mock_datetime_class.now.return_value = mock_now

  mock_module = MagicMock()
  mock_module.datetime = mock_datetime_class
  mock_module.timedelta = datetime.timedelta

  monkeypatch.setattr("managers.darkmode_mgr.datetime", mock_module)

  mock_slot = MagicMock()
  mgr.darkmode_signal.connect(mock_slot)

  mgr.check_dark_mode()

  mock_slot.assert_called_once_with(expected_darkmode)
  ctx["timer"].assert_called_once_with(30000, mgr.check_dark_mode)


def test_suntime_bug_day_shift(clean_darkmode_mgr, monkeypatch):
  """Verifies that if sunset is calculated as earlier than sunrise, it shifts 1 day forward safely."""
  ctx = clean_darkmode_mgr
  mgr = ctx["initializer"]()

  config_dict = {
    'user': {'home_lat': 32.7, 'home_lon': -117.1},
    'darkmode': {'poll_interval': 10}
  }
  mgr.set_config(config_dict)
  ctx["timer"].reset_mock()

  mock_now_aware = MagicMock()
  mock_now = MagicMock(spec=datetime.datetime)
  mock_now.astimezone.return_value = mock_now_aware

  # Bug Scenario: Suntime library miscalculates and returns Sunset (5) before Sunrise (6)
  mock_sunrise = MagicMock()
  mock_sunrise.astimezone.return_value = 6

  mock_sunset = MagicMock()
  mock_sunset.astimezone.return_value = 5

  # Simulate: local_sunset < local_sunrise evaluates to True
  mock_sunset.__lt__ = lambda self, other: True

  # Simulate adding 1 day (+1 day pushes sunset value forward mathematically to 29)
  mock_sunset.__iadd__ = lambda self, other: mock_sunset
  mock_sunset.astimezone.return_value = 29

  # Freeze 'now' time value at 10:00 PM (22)
  mock_now_aware.__ge__ = lambda self, other: 22 >= other  # 6 <= 22 -> True
  mock_now_aware.__le__ = lambda self, other: 22 <= 29  # 22 <= 29 -> True

  ctx["sun_instance"].get_sunrise_time.return_value = mock_sunrise
  ctx["sun_instance"].get_sunset_time.return_value = mock_sunset

  # Create modular mock objects for datetime tracking instead of local syntax classes
  mock_datetime_class = MagicMock()
  mock_datetime_class.now.return_value = mock_now

  mock_module = MagicMock()
  mock_module.datetime = mock_datetime_class
  mock_module.timedelta = datetime.timedelta

  monkeypatch.setattr("managers.darkmode_mgr.datetime", mock_module)

  mock_slot = MagicMock()
  mgr.darkmode_signal.connect(mock_slot)

  mgr.check_dark_mode()

  # 22 is between 6 and 29 -> evaluates to Daytime (False)
  mock_slot.assert_called_once_with(False)
