class UserConfig:
  def __init__(self, **kwargs):
    self.lat = kwargs.get("lat", 32.0)
    self.lon = kwargs.get('lon', -117.0)
    self.radius = kwargs.get('radius', 60)


class AppConfig:
  def __init__(self, **kwargs):
    self.width = kwargs.get('width', 1024)
    self.height = kwargs.get('height', 600)
    self.max_airline_name_length = kwargs.get('max_airline_name_length', 30)
    self.airline_logo_url = kwargs.get('airline_logo_url', "https://www.flightaware.com/images/airline_logos/180px/")
    self.airline_logo_url_ext = kwargs.get('airline_logo_url_ext', ".png")
    self.ui_file_name = kwargs.get('ui_file_name', "flight-tracker.ui")
    self.airlines_only = kwargs.get('airlines_only', True)
    self.has_position = kwargs.get('has_position', True)
    self.on_ground = kwargs.get('on_ground', False)
    self.has_stale_age_seconds = kwargs.get("has_stale_age_seconds", 60)
    self.has_origin_destination = kwargs.get('has_origin_destination', True)
    self.display_new_flight_interval = kwargs.get('display_new_flight_interval', 12)
    self.get_flight_list_interval = kwargs.get('get_flight_list_interval', 10)
    self.get_dark_mode_interval = kwargs.get('get_dark_mode_interval', 60)
    self.airplanes_live_reg_interval = kwargs.get('airplanes_live_reg_interval', 1.5)
    self.lookup_detail_interval = kwargs.get('lookup_detail_interval', 5)
    self.clean_interval = kwargs.get('clean_interval', 30)
    self.update_flight_list = kwargs.get('update_flight_list', 5)


class ADSBServer:
  def __init__(self, **kwargs):
    self.name = kwargs.get("name", f"adsb_server{kwargs.get('server_number', 0)}")
    self.url = kwargs.get("url")
    self.data_path = kwargs.get("data_path")
    self.interval = kwargs.get("interval", 10)
    self.is_enabled = kwargs.get("is_enabled", False)
    self.server_number = kwargs.get("server_number", 0)


user_config = UserConfig(lat=32.800016, lon=-117.052769, radius=60)
airplanes_live_server = ADSBServer(
  server_number=0,
  name="airplanes.live",
  url=f"https://api.airplanes.live/v2/point/{user_config.lat}/{user_config.lon}/{user_config.radius}",
  data_path="ac",
  interval=10,
  stale_age=60,
  is_enabled=False)
flightaware_server = ADSBServer(
  server_number=1,
  name="flightAware",
  url="http://192.168.0.64:8080/data/aircraft.json",
  data_path="aircraft",
  interval=1,
  stale_age=60,
  is_enabled=True)
piaware_server = ADSBServer(
  server_number=2,
  name="piAware",
  url="http://192.168.0.42:8080/data-978/aircraft.json",
  data_path="aircraft",
  interval=1,
  stale_age=60,
  is_enabled=False)


class Config:
  def __init__(self, **kwargs):
    self.user = UserConfig(lat=32.800016, lon=-117.052769, radius=60)
    self.app = AppConfig()
    self.adsb_servers = [airplanes_live_server, flightaware_server, piaware_server]
    self.check_config(self.user, self.app)

  def check_config(self, user: UserConfig, app: AppConfig):
    lat = user.lat
    lon = user.lon
    radius = user.radius
    width = app.width
    height = app.height
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
      raise Exception("InvalidLatLon")
    if not (0 < float(radius) <= 10000):
      raise Exception("RadiusOutOfRange")
    if width is None or height is None:
      raise Exception("UnspecifiedSize")
    if not (width > 0 and height > 0):
      raise Exception("InvalidSize")
    return True
