import logging
from pathlib import Path
from app import App
from utilities import TextSuppressionFilter


def main():
  # Get the app base folder first
  base_path = Path(__file__).resolve().parent

  # Set up logging
  logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
  my_filter = TextSuppressionFilter()
  root_logger = logging.getLogger()
  root_logger.addFilter(my_filter)
  for handler in root_logger.handlers:
    handler.addFilter(my_filter)

  # Start the app!
  App(base_path=base_path, logger=root_logger)
