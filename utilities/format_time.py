from datetime import datetime
from zoneinfo import ZoneInfo


# Return tuple of (timestamp, time_string, tz_abbr)
def format_time(timestamp: int, tz_name: str, tz_abbr: str) -> tuple[int, str]:
  # Converts seconds past epoch to "HH:MM" in the specified time zone
  time_str = f"{datetime.fromtimestamp(timestamp, tz=ZoneInfo(tz_name)).strftime("%H:%M")} {tz_abbr}"
  return timestamp, time_str
