import pytest
from unittest.mock import MagicMock
from PySide6.QtCore import QObject

# Import your actual classes here
from managers.config_mgr import ConfigMgr


class FakeMgr(QObject):
  """A clean, real PySide6 QObject to serve as a safe base class for testing."""

  def __init__(self, base_path, logger):
    super().__init__()
    self.base_path = base_path
    self.logger = logger


@pytest.fixture
def clean_config_mgr(monkeypatch):
  """Safely constructs ConfigMgr by substituting the parent class with a real QObject."""
  # This safely intercepts the parent constructor, keeping PySide/C++ happy
  monkeypatch.setattr("managers.config_mgr.Mgr", FakeMgr)

  # Create a fully mockable configuration parser mock structure
  mock_parser = MagicMock()
  monkeypatch.setattr("managers.config_mgr.BooleanConfigParser", lambda *args, **kwargs: mock_parser)

  def _initializer(sections_data):
    # Setup mock behavior for configparser dictionary access loops
    mock_parser.sections.return_value = list(sections_data.keys())
    mock_parser.defaults.return_value = []
    mock_parser.__getitem__.side_effect = lambda section: sections_data.get(section, {})

    # Instantiate with safe keyword args
    return ConfigMgr(base_path="/fake/path", logger=MagicMock(), config_file="config.ini")

  return _initializer


def test_config_mgr_success(clean_config_mgr):
  """Verifies successful loading, dictionary parsing, and data retrieval methods."""
  valid_data = {
    'user': {'home_lat': '45.0', 'home_lon': '-75.0', 'home_radius': '500'},
    'system': {'theme': 'dark'}
  }

  mgr = clean_config_mgr(valid_data)

  # Assert retrieval methods function correctly
  assert mgr.get_config_value('user', 'home_lat') == '45.0'
  assert mgr.get_config_group('system') == {'theme': 'dark'}
  assert mgr.get_config_value('nonexistent', 'key') is None


def test_config_mgr_missing_keys(clean_config_mgr):
  """Verifies that missing required lat/lon/radius keys emits the correct error."""
  invalid_data = {
    'user': {'home_lat': '45.0'}  # missing home_lon and home_radius
  }

  # Create a spy slot to watch signal emissions
  mock_slot = MagicMock()

  # We patch is_valid_config out for a brief millisecond to connect our signal safely
  with pytest.MonkeyPatch.context() as mp:
    mp.setattr(ConfigMgr, "is_valid_config", lambda self: None)
    mgr = clean_config_mgr(invalid_data)

  mgr.invalid_config.connect(mock_slot)
  is_valid_config()  # Manually run the calculation now that the signal is bound

  mock_slot.assert_called_once_with("ConfigError-LatLonRadiusMissing")


@pytest.mark.parametrize(
  "lat,lon,expected_error", [
    ("91.0", "0.0", "ConfigError-InvalidLatLon"),
    ("-90.1", "0.0", "ConfigError-InvalidLatLon"),
    ("0.0", "180.1", "ConfigError-InvalidLatLon"),
    ("0.0", "-180.1", "ConfigError-InvalidLatLon"),
  ])
def test_config_mgr_invalid_coordinates(clean_config_mgr, lat, lon, expected_error):
  """Verifies coordinate boundaries and their respective error emissions."""
  invalid_data = {
    'user': {'home_lat': lat, 'home_lon': lon, 'home_radius': '100'}
  }

  mock_slot = MagicMock()
  with pytest.MonkeyPatch.context() as mp:
    mp.setattr(ConfigMgr, "is_valid_config", lambda self: None)
    mgr = clean_config_mgr(invalid_data)

  mgr.invalid_config.connect(mock_slot)
  is_valid_config()

  mock_slot.assert_called_once_with(expected_error)


@pytest.mark.parametrize("radius", ["0", "-5", "10000.1"])
def test_config_mgr_invalid_radius(clean_config_mgr, radius):
  """Verifies radius boundaries and out-of-range error emissions."""
  invalid_data = {
    'user': {'home_lat': '0.0', 'home_lon': '0.0', 'home_radius': radius}
  }

  mock_slot = MagicMock()
  with pytest.MonkeyPatch.context() as mp:
    mp.setattr(ConfigMgr, "is_valid_config", lambda self: None)
    mgr = clean_config_mgr(invalid_data)

  mgr.invalid_config.connect(mock_slot)
  is_valid_config()

  mock_slot.assert_called_once_with("ConfigError-RadiusOutOfRange")


def test_config_mgr_signals_can_connect(clean_config_mgr):
  """Verifies that new class-level signals exist and safely accept Qt connections."""
  valid_data = {
    'user': {'home_lat': '45.0', 'home_lon': '-75.0', 'home_radius': '500'}
  }
  mgr = clean_config_mgr(valid_data)

  mock_slot = MagicMock()

  # Ensure both signals exist and function as true Qt Signals
  mgr.send_config_dict.connect(mock_slot)
  mgr.invalid_config.connect(mock_slot)
