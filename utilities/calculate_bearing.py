# /**
#  * Calculates the bearing in degrees between two geographic points.
#  * @param {number} lat1 Latitude of the start point in decimal degrees.
#  * @param {number} lon1 Longitude of the start point in decimal degrees.
#  * @param {number} lat2 Latitude of the end point in decimal degrees.
#  * @param {number} lon2 Longitude of the end point in decimal degrees.
#  * @returns {number} The bearing in degrees, ranging from 0 to 360 (clockwise from North).
#  */
import math


def to_radians(deg: float) -> float:
  return deg * (math.pi / 180)


def to_degrees(rad: float) -> float:
  return (rad * 180) / math.pi


def calculate_bearing(lat1, lon1, lat2, lon2):
  # export const calculateBearing = (
  #   lat1: number,
  #   lon1: number,
  #   lat2: number,
  #   lon2: number,
  # ) => {
  #   // Convert degrees to radians
  phi1 = to_radians(lat1)
  phi2 = to_radians(lat2)
  delta_lon = to_radians(lon2 - lon1)

  # Calculate components for atan2
  y = math.sin(delta_lon) * math.cos(phi2)
  x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lon);

  # Use Math.atan2 to get the bearing in radians, then convert to degrees
  _bearing = math.atan2(y, x)
  _bearing = to_degrees(_bearing)

  # Normalize the bearing to a 0-360 degree range (clockwise from North)
  return (_bearing + 360) % 360


def calculate_direction(bearing: float):
  directions = [
    {"s": 0, "e": 11.25, "d": "N"},
    {"s": 11.25, "e": 33.75, "d": "NNE"},
    {"s": 33.75, "e": 56.25, "d": "NE"},
    {"s": 56.25, "e": 78.75, "d": "ENE"},
    {"s": 78.75, "e": 101.25, "d": "E"},
    {"s": 101.25, "e": 123.75, "d": "ESE"},
    {"s": 123.75, "e": 146.25, "d": "SE"},
    {"s": 146.25, "e": 168.75, "d": "SSE"},
    {"s": 168.75, "e": 191.25, "d": "S"},
    {"s": 191.25, "e": 213.75, "d": "SSW"},
    {"s": 213.75, "e": 236.25, "d": "SW"},
    {"s": 236.25, "e": 258.75, "d": "WSW"},
    {"s": 258.75, "e": 281.25, "d": "W"},
    {"s": 281.25, "e": 303.75, "d": "WNW"},
    {"s": 303.75, "e": 326.25, "d": "NW"},
    {"s": 326.25, "e": 348.75, "d": "NNW"},
    {"s": 348.75, "e": 360, "d": "N"},
  ];
  match = next((direction for direction in directions if direction["s"] <= bearing < direction['e']), '')
  return match['d']
