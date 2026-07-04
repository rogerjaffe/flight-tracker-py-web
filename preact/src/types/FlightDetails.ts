export interface TopLeft {
  airline_icao: string;
  callsign: string;
  aircraft_code: string;
}

export interface TopMiddle {
  origin_iata: string;
  origin_city: string;
  origin_dx: number;
  destination_iata: string;
  destination_city: string;
  destination_dx: number;
}

export interface TopRight {
  airline_text: string;
  altitude: [number, string, string, string]; // value, units, arrow, "inc"/"dec"/""
  groundspeed: [number, string, string, string]; // value, units, arrow, "inc"/"dec"/""
  heading: [number, string, string, string]; // value, units, arrow, "inc"/"dec"/""
  squawk: string;
  icao: string;
  registration: string;
  position: string;
  aircraft_type: string;
  flight_time: string;
  scheduled: [string, string, string, string]; // dep_time, dep_tz_abbr, arr_time, arr_tz_abbr
  actual_eta: [string, string, string, string, boolean, boolean]; // act, act_tz, eta, eta_tz, is_act_late, is_eta_late
  deviation: [string, string, boolean, boolean]; // act, eta, is_act_late, is_eta_late
  distance: [number, string]; // distance, units
  bearing: [number, string]; // bearing, compass
  observed: string;
}

export interface FlightDetails {
  top_left: TopLeft;
  top_middle: TopMiddle;
  top_right: TopRight;
}
