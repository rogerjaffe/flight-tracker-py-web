import type { Fr24FlightDetail } from "./Fr24FlightDetail.ts";

export interface Position {
  ground_speed: number;
  altitude: number;
  heading: number;
  latitude: number;
  longitude: number;
  squawk: string;
  timestamp: number;
  vertical_speed: number;
}

export interface Flight {
  aircraft_code: string;
  airline_iata: string;
  airline_icao: string;
  altitude: number;
  callsign: string;
  destination_airport_iata: string;
  ground_speed: number;
  heading: number;
  hex: string;
  icao_24bit: string;
  id: string;
  latitude: number;
  longitude: number;
  number: string;
  on_ground: number;
  origin_airport_iata: string;
  registration: string;
  squawk: string;
  time: number;
  vertical_speed: number;
}

export interface FlightRecord {
  flight: Flight;
  hex: string;
  position: Position[];
}

export interface BackendFlightPayload {
  flight_list: {
    [key: string]: FlightRecord;
  };
  detail: Fr24FlightDetail;
  to_display: FlightRecord;
}
