import pytest
from unittest.mock import MagicMock
from PySide6.QtCore import QObject

# Assuming your file is named managers/mgr.py
from managers.mgr import Mgr


def test_mgr_initialization_defaults():
  """Verifies that the Mgr class initializes correct state with default parameters."""
  mock_logger = MagicMock()
  base_path = "/fake/project/path"

  # Initialize using defaults
  mgr = Mgr(logger=mock_logger, base_path=base_path)

  # Assert structural elements are intact
  assert isinstance(mgr, QObject)
  assert mgr.logger == mock_logger
  assert mgr.base_path == base_path
  assert mgr.name == "MGR:anonymous"
  assert mgr.running is False
  assert mgr.is_running() is False


def test_mgr_initialization_custom_name():
  """Verifies that providing a custom name prefixes it correctly."""
  mgr = Mgr(logger=MagicMock(), base_path="/fake/path", name="flight_tracker")

  assert mgr.name == "MGR:flight_tracker"


def test_mgr_activate():
  """Verifies that activation toggles the running property and logs the event."""
  mock_logger = MagicMock()
  mgr = Mgr(logger=mock_logger, base_path="/fake/path", name="worker")

  # Action
  mgr.activate()

  # Assert state mutation
  assert mgr.running is True
  assert mgr.is_running() is True

  # Assert log payload matching custom prefix behavior
  mock_logger.info.assert_called_once_with("MGR:worker-ACTIVATE")
