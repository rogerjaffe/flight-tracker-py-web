from typing import TypedDict


class TopLeft(TypedDict):
  airline_icao: str
  callsign: str
  aircraft_code: str


class TopMiddle(TypedDict):
  origin_iata: str
  origin_city: str
  destination_iata: str
  destination_city: str


class TopRight(TypedDict):
  airline_text: str
  flight_number: str
  # altitude: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
  # groundspeed: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
  # heading: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
  squawk: str
  icao: str
  registration: str
  aircraft_type: str
  country: str
  flight_time: list  # sched_flight_time, act_flight_time, is_late
  scheduled: list  # dep_time, dep_tz_abbr, arr_time, arr_tz_abbr
  actual: list  # act, act_tz, eta, eta_tz, is_act_late, is_eta_late
  deviation: list  # act, eta, is_act_late, is_eta_late
  # distance: tuple[int, str]  # distance, units
  # bearing: tuple[int, str]  # bearing, compass
  # observed: str


class UIStaticFlightDetails(TypedDict):
  top_left: TopLeft
  top_middle: TopMiddle
  top_right: TopRight


class UIStaticListDetails(TypedDict):
  hex_code: str
  callsign: str
  origin: str
  dest: str


class UIRealTimeDetails(TypedDict):
  alt: str
  alt_arrow: str
  alt_class: str
  gs: str
  gs_arrow: str
  gs_class: str
  hdg: str
  hdg_arrow: str
  hdg_class: str
  origin_dx: int
  destination_dx: int
  position: str
  progress: int
  squawk: str
