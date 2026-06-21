from dataclasses import dataclass


@dataclass
class Fr24Flight:
  aircraft_code: str
  airline_iata: str
  airline_icao: str
  altitude: int
  callsign: str
  destination_airport_iata: str
  ground_speed: int
  heading: int
  hex: str
  icao_24bit: str
  id: str  # FR24 ID
  latitude: float
  longitude: float
  number: str
  on_ground: int
  origin_airport_iata: str
  registration: str
  squawk: str
  time: int
  vertical_speed: int
