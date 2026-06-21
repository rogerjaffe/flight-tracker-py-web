import re
from FlightRadarAPI import FlightRadar24API
from classes import Service

regex_pattern = re.compile(r'^[A-Z]{3}[0-9]{1,4}$')


class SvcGetFlights(Service):
  def __init__(self, queue, lat: float, lon: float, radius: float, name: str = "anonymous"):
    super().__init__(name=name)
    self.home_lat = lat
    self.home_lon = lon
    self.home_radius = radius
    self.queue = queue
    self.fr_api = FlightRadar24API()
    self.bounds = self.fr_api.get_bounds_by_point(self.home_lat, self.home_lon, self.home_radius * 1000)

  def process(self):
    flights = self.fr_api.get_flights(bounds=self.bounds)
    for flight in flights:
      flight.hex = flight.icao_24bit
    self.queue.put({"type": "ADD_FLIGHTS", "data": flights})
