import math

METERS_TO_KM = 0.001;
METERS_TO_MI = 0.000621371;
METERS_TO_NM = 0.000539957;


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float, units: str):
  r = 6371e3  # Earth's radius in meters
  phi1 = (lat1 * math.pi) / 180  # convert to radians
  phi2 = (lat2 * math.pi) / 180
  delta_phi = ((lat2 - lat1) * math.pi) / 180
  delta_gamma = ((lon2 - lon1) * math.pi) / 180

  a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(
    delta_gamma / 2) * math.sin(delta_gamma / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));

  meters = r * c  # Distance in meters
  match units:
    case "m":
      return meters
    case "km":
      return meters * METERS_TO_KM
    case "mi":
      return meters * METERS_TO_MI
    case "nm":
      return meters * METERS_TO_NM
    case _:
      return ""
