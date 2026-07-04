from typing import Optional
from FlightRadarAPI import Flight

from classes import ADSB
from utilities import calculate_distance, calculate_bearing, sec_to_hhmmss


def get_direction(x0: float | int, x1: float | int) -> str:
  return 'inc' if x0 < x1 else 'dec' if x0 > x1 else ''


class FtPosition:
  def __init__(self, flight: Flight, adsb: list[ADSB], config):
    last_idx = len(adsb) - 1
    prev_idx = last_idx - 1 if last_idx > 0 else 0
    last_adsb = adsb[prev_idx]
    first_adsb = adsb[0]
    self.altitude = flight.altitude
    self.altitude_dir = get_direction(last_adsb.altitude, flight.altitude)
    self.ground_speed = flight.ground_speed
    self.ground_speed_dir = get_direction(last_adsb.ground_speed, flight.ground_speed)
    self.heading = flight.heading
    self.heading_dir = get_direction(last_adsb.heading, flight.heading)
    self.vertical_speed = flight.vertical_speed
    self.vertical_speed_dir = get_direction(last_adsb.vertical_speed, flight.vertical_speed)
    self.latitude = flight.latitude
    self.longitude = flight.longitude
    self.time = flight.time
    self.distance = calculate_distance(config['home_lat'], config['home_lon'], flight.latitude, flight.longitude, 'mi')
    self.bearing = calculate_bearing(config['home_lat'], config['home_lon'], flight.latitude, flight.longitude)
    self.observed = last_adsb.time - first_adsb.time
    self.observed_text = sec_to_hhmmss(self.observed)
