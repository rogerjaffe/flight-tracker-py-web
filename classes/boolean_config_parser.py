# 1. Define the custom subclass that handles the automatic boolean conversion
import configparser


class BooleanConfigParser(configparser.ConfigParser):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Standard boolean strings recognized by ConfigParser
    self.bool_mapping = {
      'true': True, 'yes': True, 'on': True, '1': True,
      'false': False, 'no': False, 'off': False, '0': False
    }

  def get(self, section, option, *args, **kwargs):
    val = super().get(section, option, *args, **kwargs)
    # Automatically convert to Python boolean if it matches
    if isinstance(val, str) and val.lower() in self.bool_mapping:
      return self.bool_mapping[val.lower()]
    return val
