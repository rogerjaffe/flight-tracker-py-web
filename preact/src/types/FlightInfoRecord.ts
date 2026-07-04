export type FlightInfoTopLeft = {
  airline_icao: string;
  callsign: string;
  aircraft_code: string;
};

export type FlightInfoTopMiddle = {
  origin_iata: string;
  origin_city: string;
  origin_dx: number;
  destination_iata: string;
  destination_city: string;
  destination_dx: number;
};

export type FlightInfoTopRight = {
  airline_text: string;
  flight_number: string;
  altitude: string;
  groundspeed: string;
  heading: string;
  country: string;
  squawk: string;
  icao: string;
  registration: string;
  position: string;
  aircraft_type: string;
  flight_time: [string, string, boolean];
  scheduled: [string, string];
  actual: [string, string, boolean, boolean];
};

export type RealTimeFlightInfo = {
  alt: string;
  alt_arrow: string;
  alt_class: string;
  gs: string;
  gs_arrow: string;
  gs_class: string;
  hdg: string;
  hdg_arrow: string;
  hdg_class: string;
  lat: number;
  lon: number;
  squawk: string;
  time: number;
  progress: number;
  origin_dx: number;
  destination_dx: number;
  position: string;
};

export type FlightInfoRecord = {
  top_left: FlightInfoTopLeft;
  top_middle: FlightInfoTopMiddle;
  top_right: FlightInfoTopRight;
  real_time: RealTimeFlightInfo;
};

// export interface FlightInfoRecord {
//   actual_dep: string;
//   actual_time: string;
//   actual_time_late: string;
//   aircraft_code: string;
//   aircraft_type: string;
//   airline_icao: string;
//   alt_arrow: string;
//   alt_class: string;
//   alt_value: string;
//   arr_is_late: string;
//   arr_late_str: string;
//   arr_lateness_str: string;
//   arr_lateness_class: string;
//   callsign: string;
//   country: string;
//   dep_is_late: string;
//   dep_late_str: string;
//   dep_lateness_str: string;
//   dep_lateness_class: string;
//   destination_city: string;
//   destination_iata: string;
//   est_arr: string;
//   flight_time: string;
//   flight_time_late: string;
//   gs_arrow: string;
//   gs_class: string;
//   gs_value: number;
//   hdg_arrow: string;
//   hdg_class: string;
//   hdg_value: number;
//   hex_code: string;
//   lat: number;
//   lat_dir: string;
//   lon: number;
//   lon_dir: string;
//   observed: string;
//   origin_city: string;
//   origin_iata: string;
//   registration: string;
//   scheduled_arr: string;
//   scheduled_dep: string;
//   squawk: number;
// }
