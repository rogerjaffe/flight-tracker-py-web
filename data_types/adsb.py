# from FlightRadarAPI import Flight


class ADSB:
  def __init__(self, flight):
    self.squawk = flight.squawk
    self.hex = flight.icao_24bit
    self.altitude = flight.altitude
    self.ground_speed = flight.ground_speed
    self.heading = flight.heading
    self.lat = flight.latitude
    self.lon = flight.longitude
    self.time = flight.time
    self.vertical_speed = flight.vertical_speed
