export interface BriefFlight {
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
