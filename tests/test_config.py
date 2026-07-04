import unittest
from typing import Any
# Assuming your source code is named flight_config.py
from config import check_config, load_config, config


class TestFlightConfig(unittest.TestCase):

  def setUp(self) -> None:
    """Create a fresh valid configuration dictionary copy before every test."""
    self.valid_config: Any = config.copy()

  def test_check_config_valid(self) -> None:
    """Should return True when all configuration parameters are completely valid."""
    result = check_config(self.valid_config)
    self.assertTrue(result)

  def test_check_config_invalid_latitude_high(self) -> None:
    """Should raise Exception('InvalidLatLon') if latitude exceeds 90 degrees."""
    self.valid_config["home_lat"] = 90.001
    with self.assertRaises(Exception) as context:
      check_config(self.valid_config)
    self.assertEqual(str(context.exception), "InvalidLatLon")

  def test_check_config_invalid_longitude_low(self) -> None:
    """Should raise Exception('InvalidLatLon') if longitude drops below -180 degrees."""
    self.valid_config["home_lon"] = -180.001
    with self.assertRaises(Exception) as context:
      check_config(self.valid_config)
    self.assertEqual(str(context.exception), "InvalidLatLon")

  def test_check_config_radius_out_of_range_high(self) -> None:
    """Should raise Exception('RadiusOutOfRange') if radius exceeds 10,000."""
    self.valid_config["home_radius"] = 10001
    with self.assertRaises(Exception) as context:
      check_config(self.valid_config)
    self.assertEqual(str(context.exception), "RadiusOutOfRange")

  def test_check_config_radius_out_of_range_zero(self) -> None:
    """Should raise Exception('RadiusOutOfRange') if radius is exactly zero or negative."""
    self.valid_config["home_radius"] = 0
    with self.assertRaises(Exception) as context:
      check_config(self.valid_config)
    self.assertEqual(str(context.exception), "RadiusOutOfRange")

  def test_check_config_invalid_dimensions(self) -> None:
    """Should raise Exception('InvalidSize') if width or height is zero or negative."""
    self.valid_config["app_width"] = 0
    with self.assertRaises(Exception) as context:
      check_config(self.valid_config)
    self.assertEqual(str(context.exception), "InvalidSize")

  def test_load_config_success(self) -> None:
    """Should return the actual config dictionary if the setup validation passes."""
    # Using the base global dictionary since it's already structured perfectly
    result = load_config()
    self.assertIn("home_lat", result)
    self.assertNotIn("error", result)
