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
    # Fetch the raw string value from the configuration file
    val = super().get(section, option, *args, **kwargs)

    if not isinstance(val, str):
      return val

    val_lower = val.lower()

    # 1. Handle Boolean Conversion
    if val_lower in self.bool_mapping:
      return self.bool_mapping[val_lower]

    # 2. Handle Integer Conversion
    try:
      return int(val)
    except ValueError:
      pass

    # 3. Handle Float Conversion
    try:
      return float(val)
    except ValueError:
      pass

    # Return original string if no conversions match
    return val
