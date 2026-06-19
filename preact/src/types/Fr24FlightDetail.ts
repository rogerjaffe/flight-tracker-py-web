export interface Fr24FlightDetail {
  aircraft: Aircraft;
  airline: Airline;
  airport: Airport;
  identification: Identification;
  owner: Owner;
  status: Status;
  time: Time;
}

export interface Aircraft {
  age: Age;
  availability: Availability;
  country: Country;
  hex: string;
  model: Model;
  registration: string;
  restricted: boolean;
  serialNo: any;
}

export interface Age {
  availability: boolean;
}

export interface Availability {
  age: boolean;
  serialNo: boolean;
}

export interface Country {
  alpha2: string;
  alpha3: string;
  id: number;
  name: string;
}

export interface Model {
  code: string;
  text: string;
}

export interface Airline {
  code: Code;
  name: string;
  short: string;
}

export interface Code {
  iata: string;
  icao: string;
}

export interface Airport {
  destination: Destination;
  origin: Origin;
  real: any;
}

export interface Destination {
  code: Code;
  name: string;
  position: Position;
  timezone: Timezone;
  visible: boolean;
}

export interface Position {
  country: Country2;
  latitude: number;
  longitude: number;
  region: Region;
}

export interface Country2 {
  code: string;
  id: number;
  name: string;
}

export interface Region {
  city: string;
}

export interface Timezone {
  abbr: string;
  abbrName: string;
  isDst: boolean;
  name: string;
  offset: number;
}

export interface Origin {
  code: Code;
  name: string;
  position: Position;
  timezone: Timezone;
  visible: boolean;
}

export interface Identification {
  callsign: string;
  codeshare: any;
  id: string;
  number: Number;
  row: number;
}

export interface Number {
  alternative: string;
  default: string;
}

export interface Owner {
  code: Code;
  name: string;
}

export interface Status {
  ambiguous: boolean;
  estimated: any;
  generic: Generic;
  icon: string;
  live: boolean;
  text: string;
}

export interface Generic {
  eventTime: EventTime;
  status: Status2;
}

export interface EventTime {
  local: number;
  utc: number;
}

export interface Status2 {
  color: string;
  diverted: any;
  text: string;
  type: string;
}

export interface Time {
  estimated: ArrDepTime;
  other: Other;
  real: ArrDepTime;
  scheduled: ArrDepTime;
}

export interface ArrDepTime {
  arrival: number;
  departure: any;
}

export interface Other {
  duration: any;
  eta: number;
  updated: number;
}
