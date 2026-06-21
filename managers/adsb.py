from dataclasses import dataclass
from typing import TypedDict, NotRequired


@dataclass
class ADSB(TypedDict):
  """Shape of ADSB data retrieved from dump1090-fa and airplanes.live"""
  hex: str  # Hex ICAO code - can generate N-number
  flight: str  # Airline flight OR registration
  alt_baro: int  # barometric altitude
  gs: int  # ground speed
  track: float  # true track over the ground
  category: str  # emitted category to id api A0=D7
  # https://skybrary.aero/articles/approach-speed-categorisation#:~:text=Category%20A:%20Speed%2090%20knots,
  # Between%20121%20and%20140%20knots.
  lat: float  # latitude
  lon: float  # longitude
  timestamp: int  # Added when data is saved to the DB

  # Optional fields (marked with ? in TypeScript)
  squawk: NotRequired[str]  # squawk code
  emergency: NotRequired[str]  # none | general | lifeguard | minfuel | nordo | unlawful | downed | reserved

  # Additional fields added during processing
  airline_iata: str
  flight_number: str

  # These fields are included in the data sent to the API
  # but they are not saved in the DB or used in the application
  # alt_geom: int  # geometric altitude
  # baro_rate: NotRequired[int]  # change of barometric altitude flight mgr
  # nav_qnh: NotRequired[int]  # altimeter setting
  # nav_altitude_mcp: NotRequired[int]  # selected altitude from flight control unit
  # nav_heading: NotRequired[int]  # selected heading
  # nav_modes: NotRequired[List[str]]  # automation modes autopilot | vnav | althold | approach | lnav | tcas
  # nic: int  # navigation integrity category
  # rc: int  # radius of containment
  # seen_pos: int  # how long ago the position was last updated
  # version: NotRequired[int]  # ADS-B version number
  # nic_baro: NotRequired[int]  # navigation integrity category for barometric altitude
  # nac_p: int  # navigation accuracy for position
  # nac_v: int  # navigation accuracy for velocity
  # sil: int  # source integrity level
  # sil_type: str  # interpretation of SIL: unknown, perhour, persample
  # gva: NotRequired[int]  # geometric vertical accuracy
  # sda: NotRequired[int]  # system design assurance
  # mlat: List[str]  # list of eidls derived from MLAT data
  # tisb: List[str]  # list of fields derived from TIS-B data
  # messages: int  # total number of Mode S messages received from this api
  # seen: int  # how long ago a message was last received (sec)
  # rssi: int  # recent average RSSI signal power is dbFS (always negative)
  # geom_rate: NotRequired[int]  # rate of change of geometric altitude f/m

  # Data not included in the piaware query
  # type: NotRequired[str]  # source of underlying message
  # r: NotRequired[str]  # api registration
  # t: NotRequired[str]  # api type
  # dbFlags: NotRequired[int]  # bitfield military=1, interesting=2, PIA=4 (privacy ICAO addr), LADD=8 (unlisted)
  # desc: NotRequired[str]  # api description
  # ownOp: NotRequired[str]  # owner / operator
  # alert: NotRequired[int]  # flight status alert bit
  # spi: NotRequired[int]  # flight status special position identification bit
  # dst: NotRequired[int]  # undocumented
  # dir: NotRequired[int]  # undocumented
  # year: NotRequired[str]  # year
  # mag_heading: NotRequired[int]  # magnetic heading
