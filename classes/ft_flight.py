from FlightRadarAPI import Flight
from classes import ADSB, FtPosition


class FtFlight:
  def __init__(self, flight: Flight, config):
    self.flight = flight
    self.config = config
    self.hex = flight.icao_24bit
    self.adsb: list[ADSB] = [ADSB(flight)]
    self.position = FtPosition(flight, self.adsb, self.config)

  def update_flight(self, flight: Flight):
    self.flight = flight
    self.adsb.append(ADSB(flight))
    self.position = FtPosition(flight, self.adsb, self.config)
