export interface ADSB {
  icao_24bit: string;
  altitude: number;
  ground_speed: number;
  track: number;
  latitude: number;
  longitude: number;
  time: number; // or Date, depending on your API structure
  vertical_speed: number;
  squawk: string;
}
