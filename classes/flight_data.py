from typing import Optional, cast

from glom import glom

from utilities import get_value_arrow_class, format_time, sec_to_hhmm, calculate_distance
from data_types.UIRealTimeDetails import UIStaticListDetails, UIStaticFlightDetails, UIRealTimeDetails, TopLeft, \
  TopMiddle, TopRight
from data_types.adsb import ADSB
from data_types.fr24_flight_detail import Fr24FlightDetail


class FlightListData(UIStaticListDetails, UIRealTimeDetails):
  pass


class FlightDashboardData(UIStaticFlightDetails, UIRealTimeDetails):
  pass


class FlightData:
  def __init__(self, hex_code: str, adsb):
    self.hex: str = hex_code
    self.reg: str = ""
    self.ignore: bool = False
    self.adsb: list[ADSB] = [adsb]
    self.fr24_detail: Optional[Fr24FlightDetail] = None
    self.list_static_detail: Optional[UIStaticListDetails] = None
    self.ui_static_detail: Optional[UIStaticFlightDetails] = None
    self.real_time_detail: Optional[UIRealTimeDetails] = None

  def add_adsb(self, adsb: ADSB):
    self.adsb.append(adsb)

  def set_detail(self, fr24_detail: Fr24FlightDetail):
    if fr24_detail is None:
      return
    self.fr24_detail = fr24_detail
    self.list_static_detail = self.get_list_static_detail()
    self.ui_static_detail = self.get_ui_regions_static_detail()

  def get_list_static_detail(self) -> Optional[UIStaticListDetails]:
    callsign = glom(self.fr24_detail, 'identification.callsign', default="")
    origin = glom(self.fr24_detail, 'airport.origin.code.iata', default="")
    dest = glom(self.fr24_detail, 'airport.destination.code.iata', default="")
    hex_code = self.hex
    result: UIStaticListDetails = {
      "callsign": callsign,
      "origin": origin,
      "dest": dest,
      "hex_code": hex_code,
    }
    return result

  def get_ui_regions_static_detail(self) -> UIStaticFlightDetails:
    fr24_detail = self.fr24_detail

    callsign = glom(fr24_detail, "identification.callsign", default="")
    flight_number = callsign[3:]
    airline_icao = callsign[:3]

    origin_tz_name = glom(fr24_detail, 'airport.origin.timezone.name', default=None)
    origin_tz_abbr = glom(fr24_detail, 'airport.origin.timezone.abbr', default=None)
    dest_tz_name = glom(fr24_detail, 'airport.destination.timezone.name', default=None)
    dest_tz_abbr = glom(fr24_detail, 'airport.destination.timezone.abbr', default=None)

    # Tuples: (timestamp, time_str)
    s_dep, s_arr, a_dep, e_arr = [
      format_time(glom(fr24_detail, 'time.scheduled.departure', default=None), origin_tz_name, origin_tz_abbr),
      format_time(glom(fr24_detail, 'time.scheduled.arrival', default=None), dest_tz_name, dest_tz_abbr),
      format_time(glom(fr24_detail, 'time.real.departure', default=None), origin_tz_name, origin_tz_abbr),
      format_time(glom(fr24_detail, 'time.estimated.arrival', default=None), dest_tz_name, dest_tz_abbr),
    ]

    # Tuple: (dep_diff, arr_diff, is_dep_late, is_arr_late
    dep_arr_diff = s_dep[0] - a_dep[0], e_arr[0] - s_arr[0], s_dep[0] - a_dep[0] > 0, e_arr[0] - s_arr[0] > 0
    dep_arr_diff_str = [sec_to_hhmm(dep_arr_diff[0]), sec_to_hhmm(dep_arr_diff[1]), dep_arr_diff[2],
                        dep_arr_diff[3]]

    # Tuple: scheduled_flight_time, actual_flight_time, is_late
    flight_times = (s_arr[0] - s_dep[0], e_arr[0] - a_dep[0], (s_arr[0] - s_dep[0]) - (e_arr[0] - a_dep[0]) > 0)
    flight_times_str = [sec_to_hhmm(flight_times[0]), sec_to_hhmm(flight_times[1]), flight_times[2]]

    top_left: TopLeft = {
      "airline_icao": airline_icao,
      "callsign": callsign,
      "aircraft_code": glom(fr24_detail, "aircraft.model.code", default="Unknown")
    }

    top_middle: TopMiddle = {
      "origin_iata": glom(fr24_detail, "airport.origin.code.iata", default="---"),
      "destination_iata": glom(fr24_detail, "airport.destination.code.iata", default="---"),
      "origin_city": glom(fr24_detail, "airport.origin.position.region.city", default="---"),
      "destination_city": glom(fr24_detail, "airport.destination.position.region.city", default="---"),
    }

    top_right: TopRight = {
      "airline_text": glom(fr24_detail, "airline.name", default="Unknown"),
      "flight_number": flight_number,
      "squawk": glom(fr24_detail, "squawk", default="---"),
      "icao": self.hex,
      "registration": self.reg,
      "country": glom(fr24_detail, "aircraft.country.alpha2", default="zz"),
      "aircraft_type": glom(fr24_detail, "aircraft.model.text", default="Unknown"),
      "flight_time": flight_times_str,
      "scheduled": [s_dep[1], s_arr[1]],
      "actual": [a_dep[1], e_arr[1], a_dep[0] - s_dep[0] > 0, e_arr[0] - s_arr[0] > 0],
      "deviation": dep_arr_diff_str,
    }

    return {
      "top_left": top_left,
      "top_middle": top_middle,
      "top_right": top_right
    }

  def update_real_time_details(self):
    adsb = self.adsb[len(self.adsb) - 1]
    fr24_detail = self.fr24_detail
    lat = adsb.get('lat', None)
    lon = adsb.get('lon', None)

    origin_dx = -1
    destination_dx = -1
    progress = -1
    if lat is not None and lon is not None:
      origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
      origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
      destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
      destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
      origin_dx = calculate_distance(origin_lat, origin_lon, lat, lon, 'mi')
      destination_dx = calculate_distance(destination_lat, destination_lon, lat, lon, 'mi')
      total_dx = origin_dx + destination_dx
      progress = round(origin_dx / total_dx * 100, 0) if total_dx != 0 else 0

    alt, alt_arrow, alt_class = get_value_arrow_class(self.adsb, 'alt_baro', 'ud')
    gs, gs_arrow, gs_class = get_value_arrow_class(self.adsb, 'gs', 'ud')
    hdg, hdg_arrow, hdg_class = get_value_arrow_class(self.adsb, 'track', 'lr')
    adsb = self.adsb[len(self.adsb) - 1]
    real_time_detail: UIRealTimeDetails = {
      "alt": alt,
      "alt_arrow": alt_arrow,
      "alt_class": alt_class,
      "gs": gs if gs != '0' else "",
      "gs_arrow": gs_arrow,
      "gs_class": gs_class,
      "hdg": hdg if hdg != 0 else "",
      "hdg_arrow": hdg_arrow,
      "hdg_class": hdg_class,
      "position": "32.1234N 117.8722W",
      "squawk": adsb.get('squawk', ''),
      "progress": progress,
      "origin_dx": origin_dx,
      "destination_dx": destination_dx,
      # "position": f"{self.lat}{self.lat_dir} {self.lon}{self.lon_dir}",
    }
    self.real_time_detail = real_time_detail

  def package_for_flight_list(self) -> FlightListData:
    self.update_real_time_details()
    if self.list_static_detail is None or self.real_time_detail is None:
      # Return an empty dict cast to FlightListData or handle as needed
      # For now, providing a safe merge that satisfies the type checker
      return cast(
        FlightListData, cast(
          object, {
            **(self.list_static_detail or {}),
            **(self.real_time_detail or {}),
          }))

    return cast(
      FlightListData, cast(
        object, {
          **self.list_static_detail,
          **self.real_time_detail,
        }))

  def package_for_flight_data(self) -> FlightDashboardData:
    self.update_real_time_details()
    return self.ui_static_detail | {"real_time": self.real_time_detail}

  # def package_flight_data(self, flight_detail: Any) -> dict[str, Any]:
  #   fr24_detail = flight_detail.detail
  #   adsbs = flight_detail.adsb
  #   if len(adsbs) == 0:
  #     squawk = ''
  #     lat = ''
  #     lon = ''
  #     lat_dir = '',
  #     lon_dir = '',
  #     observed = '0m 0s'
  #   else:
  #     last_adsb = adsbs[-1]
  #     first_adsb = adsbs[0]
  #     squawk = last_adsb.get('squawk', None)
  #     lat, lat_dir = decode_position(adsbs, 'lat')
  #     lon, lon_dir = decode_position(adsbs, 'lon')
  #     observed = sec_to_hhmmss(last_adsb.get('time', 0) - first_adsb.get('time', 0))
  #
  #   alt_value, alt_arrow, alt_class = get_value_arrow_class(adsbs, 'alt_baro', 'ud')
  #   gs_value, gs_arrow, gs_class = get_value_arrow_class(adsbs, 'gs', 'lr')
  #   hdg_value, hdg_arrow, hdg_class = get_value_arrow_class(adsbs, 'heading', 'lr')
  #
  #   hex_code = glom(fr24_detail, "aircraft.hex", default="---")
  #   registration = glom(fr24_detail, 'aircraft.registration', default="---")
  #   aircraft_type = glom(fr24_detail, 'aircraft.model.text', default="---")
  #   callsign = glom(fr24_detail, 'identification.callsign', default="Unknown")
  #   callsign_str = f"{callsign[:3]}{callsign[3:]}"
  #   airline_icao = glom(fr24_detail, 'airline.code.icao', default="UNK")
  #   aircraft_code = glom(fr24_detail, 'aircraft.model.code', default="")
  #   aircraft_country = glom(fr24_detail, 'aircraft.country.alpha2', default="ZZ")
  #   origin_iata = glom(fr24_detail, 'airport.origin.code.iata', default="---")
  #   origin_city = glom(fr24_detail, 'airport.origin.position.region.city', default="---")
  #   destination_iata = glom(fr24_detail, 'airport.destination.code.iata', default="---")
  #   destination_city = glom(fr24_detail, 'airport.destination.position.region.city', default="---")
  #
  #   scheduled_dep = glom(fr24_detail, 'time.scheduled.departure', default=None)
  #   scheduled_arr = glom(fr24_detail, 'time.scheduled.arrival', default=None)
  #   actual_dep = glom(fr24_detail, 'time.real.departure', default=None)
  #   est_arr = glom(fr24_detail, 'time.estimated.arrival', default=None)
  #
  #   # tz is "America/New_York"
  #   dep_tz = glom(fr24_detail, 'airport.origin.timezone.name', default=None)
  #   arr_tz = glom(fr24_detail, 'airport.destination.timezone.name', default=None)
  #
  #   # tz_abbr is "EDT"
  #   dep_tz_abbr = glom(fr24_detail, 'airport.origin.timezone.abbr', default="")
  #   arr_tz_abbr = glom(fr24_detail, 'airport.destination.timezone.abbr', default="")
  #
  #   scheduled_dep_str = format_time(scheduled_dep, dep_tz, dep_tz_abbr) if scheduled_dep is not None else "---"
  #   scheduled_arr_str = format_time(scheduled_arr, arr_tz, arr_tz_abbr) if scheduled_arr is not None else "---"
  #   actual_dep_str = format_time(actual_dep, dep_tz, dep_tz_abbr) if actual_dep != 0 else "---"
  #   est_arr_str = format_time(est_arr, arr_tz, arr_tz_abbr) if est_arr != 0 else "---"
  #
  #   if (scheduled_dep is not None and scheduled_arr is not None) and (actual_dep is not None and est_arr is not None):
  #     flight_time = scheduled_arr - scheduled_dep
  #     actual_time = est_arr - actual_dep
  #     dep_late = actual_dep - scheduled_dep
  #     arr_late = est_arr - scheduled_arr
  #     flight_time_str = sec_to_hhmmss(flight_time) if scheduled_arr != 0 and scheduled_dep != 0 else ""
  #     actual_time_str = sec_to_hhmmss(actual_time) if est_arr != 0 and actual_dep != 0 else ""
  #     actual_time_late = has_late(flight_time, actual_time)
  #     dep_is_late = has_late(scheduled_dep, actual_dep)
  #     arr_is_late = has_late(scheduled_arr, est_arr)
  #     flight_time_late = has_late(
  #       flight_time,
  #       actual_time
  #     )
  #     dep_lateness = scheduled_dep - actual_dep
  #     arr_lateness = scheduled_arr - est_arr
  #     dep_lateness_str = sec_to_hhmmss(dep_lateness)
  #     arr_lateness_str = sec_to_hhmmss(arr_lateness)
  #     dep_lateness_class = 'late' if dep_lateness < 0 else ''
  #     arr_lateness_class = 'late' if arr_lateness < 0 else ''
  #     origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
  #     origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
  #     destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
  #     destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
  #   else:
  #     flight_time_str = "---"
  #     actual_time_str = "---"
  #     dep_late = 0
  #     arr_late = 0
  #     actual_time_late = False
  #     dep_is_late = False
  #     arr_is_late = False
  #     flight_time_late = '---'
  #     dep_lateness_str = "---"
  #     arr_lateness_str = "---"
  #     dep_lateness_class = ''
  #     arr_lateness_class = ''
  #     origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
  #     origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
  #     destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
  #     destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
  #
  #   return {
  #     "hex_code": hex_code,
  #     "registration": registration,
  #     "squawk": squawk,
  #     "aircraft_type": aircraft_type,
  #     "callsign": callsign_str,
  #     "airline_icao": airline_icao,
  #     "aircraft_code": aircraft_code,
  #     "country": aircraft_country,
  #     "origin_iata": origin_iata,
  #     "origin_city": origin_city,
  #     'lat': lat,
  #     'lon': lon,
  #     'lat_dir': lat_dir,
  #     'lon_dir': lon_dir,
  #
  #     "alt_value": alt_value,
  #     "alt_arrow": alt_arrow,
  #     "alt_class": alt_class,
  #     "gs_value": gs_value,
  #     "gs_arrow": gs_arrow,
  #     "gs_class": gs_class,
  #     "hdg_value": hdg_value,
  #     "hdg_arrow": hdg_arrow,
  #     "hdg_class": hdg_class,
  #
  #     "destination_iata": destination_iata,
  #     "destination_city": destination_city,
  #     "scheduled_dep": scheduled_dep_str,
  #     "scheduled_arr": scheduled_arr_str,
  #     "actual_dep": actual_dep_str,
  #     "est_arr": est_arr_str,
  #     "flight_time": flight_time_str,
  #     "actual_time": actual_time_str,
  #     "dep_late_str": sec_to_hhmmss(abs(dep_late)) if dep_late > 0 else "---",
  #     "arr_late_str": sec_to_hhmmss(abs(arr_late)) if arr_late > 0 else "---",
  #     "flight_time_late": flight_time_late,
  #     "dep_is_late": dep_is_late,
  #     "arr_is_late": arr_is_late,
  #     "actual_time_late": actual_time_late,
  #     "dep_lateness_str": dep_lateness_str,
  #     "arr_lateness_str": arr_lateness_str,
  #     "dep_lateness_class": dep_lateness_class,
  #     "arr_lateness_class": arr_lateness_class,
  #     "observed": observed,
  #   }
