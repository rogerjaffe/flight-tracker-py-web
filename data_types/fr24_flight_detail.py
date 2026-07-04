from dataclasses import dataclass
from typing import Any, TypedDict


@dataclass
class Age(TypedDict):
  availability: bool


@dataclass
class Availability(TypedDict):
  age: bool
  serialNo: bool


@dataclass
class Country(TypedDict):
  alpha2: str
  alpha3: str
  id: int
  name: str


@dataclass
class Model(TypedDict):
  code: str
  text: str


@dataclass
class Aircraft(TypedDict):
  age: Age
  availability: Availability
  country: Country
  hex: str
  model: Model
  registration: str
  restricted: bool
  serialNo: Any  # Replaces 'any'


@dataclass
class Code(TypedDict):
  iata: str
  icao: str


@dataclass
class Airline(TypedDict):
  code: Code
  name: str
  short: str


@dataclass
class Country2(TypedDict):
  code: str
  id: int
  name: str


@dataclass
class Region(TypedDict):
  city: str


@dataclass
class Position(TypedDict):
  country: Country2
  latitude: float
  longitude: float
  region: Region


@dataclass
class Timezone(TypedDict):
  abbr: str
  abbrName: str
  isDst: bool
  name: str
  offset: int


@dataclass
class Destination(TypedDict):
  code: Code
  name: str
  position: Position
  timezone: Timezone
  visible: bool


@dataclass
class Origin(TypedDict):
  code: Code
  name: str
  position: Position
  timezone: Timezone
  visible: bool


@dataclass
class Airport(TypedDict):
  destination: Destination
  origin: Origin
  real: Any  # Replaces 'any'


@dataclass
class FlightNumber:  # Renamed from 'Number' to avoid collision with Python built-in(TypedDict)s
  alternative: str
  default: str


@dataclass
class Identification(TypedDict):
  callsign: str
  codeshare: Any  # Replaces 'any'
  id: str
  number: FlightNumber
  row: int


@dataclass
class Owner(TypedDict):
  code: Code
  name: str


@dataclass
class EventTime(TypedDict):
  local: int
  utc: int


@dataclass
class Status2(TypedDict):
  color: str
  diverted: Any  # Replaces 'any'
  text: str
  type: str


@dataclass
class Generic(TypedDict):
  eventTime: EventTime
  status: Status2


@dataclass
class Status(TypedDict):
  ambiguous: bool
  estimated: Any  # Replaces 'any'
  generic: Generic
  icon: str
  live: bool
  text: str


@dataclass
class ArrDepTime(TypedDict):
  arrival: int
  departure: Any  # Replaces 'any'


@dataclass
class Other(TypedDict):
  duration: Any  # Replaces 'any'
  eta: int
  updated: int


@dataclass
class Time(TypedDict):
  estimated: ArrDepTime
  other: Other
  real: ArrDepTime
  scheduled: ArrDepTime


@dataclass
class Fr24FlightDetail(TypedDict):
  aircraft: Aircraft
  airline: Airline
  airport: Airport
  identification: Identification
  owner: Owner
  status: Status
  time: Time
