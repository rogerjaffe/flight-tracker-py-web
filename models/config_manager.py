import configparser
import os

from classes import BooleanConfigParser


class ConfigManager:
  def __init__(self, base_path, config_file):
    # Read config.ini information
    self.base_path = base_path
    config_path = os.path.join(self.base_path, 'config.ini')
    self.config = BooleanConfigParser(interpolation=configparser.ExtendedInterpolation())
    self.config.read(config_path)

  def get_config(self):
    config_dict = {
      section: {k: v for k, v in self.config[section].items() if k not in self.config.defaults()}
      for section in self.config.sections()
    }
    return config_dict

  def get_config_group(self, group_name: str):
    return self.get_config()[group_name]

  def get_config_value(self, group_name: str, key: str):
    return self.get_config_group(group_name)[key]
