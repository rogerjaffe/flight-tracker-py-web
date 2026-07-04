from typing import Any


def to_plain_dict(value: Any):
  if value is None or isinstance(value, (str, int, float, bool)):
    return value

  if isinstance(value, list):
    return [to_plain_dict(item) for item in value]

  if isinstance(value, tuple):
    return [to_plain_dict(item) for item in value]

  if isinstance(value, dict):
    return {
      str(key): to_plain_dict(item)
      for key, item in value.items()
    }

  if hasattr(value, "__dict__"):
    return {
      key: to_plain_dict(item)
      for key, item in vars(value).items()
      if not key.startswith("_")
    }

  return str(value)
