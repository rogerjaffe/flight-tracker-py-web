export interface UserConfig {
  lat: number;
  lon: number;
  radius: number;
}

export interface AppConfig {
  width: number;
  height: number;
  max_airline_name_length: number;
  airline_logo_url: string;
  airline_logo_url_ext: string;
  ui_file_name: string;
  airlines_only: boolean;
  has_position: boolean;
  on_ground: boolean;
  has_stale_age_seconds: number;
  has_origin_destination: boolean;
  display_new_flight_interval: number;
  get_flight_list_interval: number;
  get_dark_mode_interval: number;
  airplanes_live_reg_interval: number;
  lookup_detail_interval: number;
  clean_interval: number;
  update_flight_list: number;
}

export interface ADSBServer {
  name: string;
  url: string | null;
  data_path: string | null;
  interval: number;
  is_enabled: boolean;
  server_number: number;
  stale_age: number; // Added since your instances utilize this property
}

export interface Config {
  user: UserConfig;
  app: AppConfig;
  adsb_servers: ADSBServer[];
}
