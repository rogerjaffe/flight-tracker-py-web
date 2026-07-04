from dataclasses import dataclass


@dataclass
class Config:
  home_lat: float = 32.800016
  home_lon: float = -117.052769
  home_radius: int = 80
  app_width: int = 1024
  app_height: int = 600
  max_airline_name_length: int = 30
  airline_logo_url: str = "https://flightaware.com"
  airline_logo_url_ext: str = ".png"
  ui_file_name: str = "flight-tracker.ui"
  airlines_only: bool = True
  has_position: bool = True
  on_ground: bool = False
  has_origin_destination: bool = True
  get_new_flight_interval: int = 12
  get_flight_list_interval: int = 10
  get_dark_mode_interval: int = 10
