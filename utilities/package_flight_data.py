from dataclasses import dataclass
from typing import Any, TypedDict

from classes import Fr24FlightDetail
from classes.flight_data import FlightData, TopLeft, TopMiddle, TopRight
from glom import glom

#
# @dataclass
# class TopLeft(TypedDict):
#   airline_icao: str
#   callsign: str
#   aircraft_code: str
#
#
# @dataclass
# class TopMiddle(TypedDict):
#   origin_iata: str
#   origin_city: str
#   origin_dx: int
#   destination_iata: str
#   destination_city: str
#   destination_dx: int
#
#
# class TopRight(TypedDict):
#   airline_text: str
#   altitude: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
#   groundspeed: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
#   heading: tuple[int, str, str, str]  # value, units, arrow, "inc"/"dec"/""
#   squawk: str
#   icao: str
#   registration: str
#   position: str
#   aircraft_type: str
#   flight_time: str
#   scheduled: tuple[str, str, str, str]  # dep_time, dep_tz_abbr, arr_time, arr_tz_abbr
#   actual_eta: tuple[str, str, str, str, bool, bool]  # act, act_tz, eta, eta_tz, is_act_late, is_eta_late
#   deviation: tuple[str, str, bool, bool]  # act, eta, is_act_late, is_eta_late
#   distance: tuple[int, str]  # distance, units
#   bearing: tuple[int, str]  # bearing, compass
#   observed: str
#
#
# @dataclass
# class FlightDetails(TypedDict):
#   top_left: TopLeft
#   top_middle: TopMiddle
#   top_right: TopRight
#

# def package_flight_data(fr24_detail: Fr24FlightDetail) -> dict[str, Any]:
#   # Top Left
#   top_left: TopLeft = {
#     "airline_icao": glom(fr24_detail, "airline.code.icao", default="UNK"),
#     "callsign": glom(fr24_detail, "identification.callsign", default="Not tracked"),
#     "aircraft_code": glom(fr24_detail, "aircraft.model.code", default="Unknown")
#   }
#
#   top_middle: TopMiddle = {
#     "origin_iata": glom(fr24_detail, "airport.origin.code.iata", default="---"),
#     "destination_iata": glom(fr24_detail, "airport.destination.code.iata", default="---"),
#     "origin_city": glom(fr24_detail, "airport.origin.position.region.city", default="---"),
#     "destination_city": glom(fr24_detail, "airport.destination.position.region.city", default="---"),
#     "origin_dx": 0,
#     "destination_dx": 0
#   }
#
#   top_right: TopRight = {
#     "airline_text": "American 1234",
#     "altitude": (12000, 'ft', "▲", 'inc'),
#     "groundspeed": (245, 'kts', "▼", 'inc'),
#     "heading": (132, "\u00B0", "◀", 'dec'),
#     "squawk": "1234",
#     "icao": "AABBCC",
#     "registration": "N90823",
#     "position": "32.5643N 117.2234W",
#     "aircraft_type": "B738",
#     "flight_time": "5h 23m",
#     "scheduled": ("14:33", "PDT", "22:45", "CET"),  # dep_time, dep_tz_abbr, arr_time, arr_tz_abbr
#     "actual_eta": ("14:35", "PDT", "20:11", "CET", False, True),  # act, act_tz, eta, eta_tz, is_act_late, is_eta_late
#     "deviation": ("4m 25s", "2m 54s", True, False),  # act, eta, is_act_late, is_eta_late
#     "distance": (23, "mi"),  # distance, units
#     "bearing": (239, "WSW"),  # bearing, compass
#     "observed": "27m 12s"
#   }
#
#   return {
#     "top_left": top_left,
#     "top_middle": top_middle,
#     "top_right": top_right
#   }

# adsbs = flight_data.adsb
# if len(adsbs) == 0:
#   squawk = ''
#   lat = ''
#   lon = ''
#   lat_dir = '',
#   lon_dir = '',
#   observed = '0m 0s'
# else:
#   last_adsb = adsbs[-1]
#   first_adsb = adsbs[0]
#   squawk = last_adsb.get('squawk', None)
#   lat, lat_dir = decode_position(adsbs, 'lat')
#   lon, lon_dir = decode_position(adsbs, 'lon')
#   observed = sec_to_hhmmss(last_adsb.get('time', 0) - first_adsb.get('time', 0))
#
# alt_value, alt_arrow, alt_class = get_value_arrow_class(adsbs, 'alt_baro', 'ud')
# gs_value, gs_arrow, gs_class = get_value_arrow_class(adsbs, 'gs', 'lr')
# hdg_value, hdg_arrow, hdg_class = get_value_arrow_class(adsbs, 'heading', 'lr')
#
# hex_code = glom(fr24_detail, "aircraft.hex", default="---")
# registration = glom(fr24_detail, 'aircraft.registration', default="---")
# aircraft_type = glom(fr24_detail, 'aircraft.model.text', default="---")
# callsign = glom(fr24_detail, 'identification.callsign', default="Unknown")
# callsign_str = f"{callsign[:3]}{callsign[3:]}"
# airline_icao = glom(fr24_detail, 'airline.code.icao', default="UNK")
# aircraft_code = glom(fr24_detail, 'aircraft.model.code', default="")
# aircraft_country = glom(fr24_detail, 'aircraft.country.alpha2', default="ZZ")
# origin_iata = glom(fr24_detail, 'airport.origin.code.iata', default="---")
# origin_city = glom(fr24_detail, 'airport.origin.position.region.city', default="---")
# destination_iata = glom(fr24_detail, 'airport.destination.code.iata', default="---")
# destination_city = glom(fr24_detail, 'airport.destination.position.region.city', default="---")
#
# scheduled_dep = glom(fr24_detail, 'time.scheduled.departure', default=None)
# scheduled_arr = glom(fr24_detail, 'time.scheduled.arrival', default=None)
# actual_dep = glom(fr24_detail, 'time.real.departure', default=None)
# est_arr = glom(fr24_detail, 'time.estimated.arrival', default=None)
#
# # tz is "America/New_York"
# dep_tz = glom(fr24_detail, 'airport.origin.timezone.name', default=None)
# arr_tz = glom(fr24_detail, 'airport.destination.timezone.name', default=None)
#
# # tz_abbr is "EDT"
# dep_tz_abbr = glom(fr24_detail, 'airport.origin.timezone.abbr', default="")
# arr_tz_abbr = glom(fr24_detail, 'airport.destination.timezone.abbr', default="")
#
# scheduled_dep_str = format_time(scheduled_dep, dep_tz, dep_tz_abbr) if scheduled_dep is not None else "---"
# scheduled_arr_str = format_time(scheduled_arr, arr_tz, arr_tz_abbr) if scheduled_arr is not None else "---"
# actual_dep_str = format_time(actual_dep, dep_tz, dep_tz_abbr) if actual_dep != 0 else "---"
# est_arr_str = format_time(est_arr, arr_tz, arr_tz_abbr) if est_arr != 0 else "---"
#
# if (scheduled_dep is not None and scheduled_arr is not None) and (actual_dep is not None and est_arr is not None):
#   flight_time = scheduled_arr - scheduled_dep
#   actual_time = est_arr - actual_dep
#   dep_late = actual_dep - scheduled_dep
#   arr_late = est_arr - scheduled_arr
#   flight_time_str = sec_to_hhmmss(flight_time) if scheduled_arr != 0 and scheduled_dep != 0 else ""
#   actual_time_str = sec_to_hhmmss(actual_time) if est_arr != 0 and actual_dep != 0 else ""
#   actual_time_late = has_late(flight_time, actual_time)
#   dep_is_late = has_late(scheduled_dep, actual_dep)
#   arr_is_late = has_late(scheduled_arr, est_arr)
#   flight_time_late = has_late(
#     flight_time,
#     actual_time
#   )
#   dep_lateness = scheduled_dep - actual_dep
#   arr_lateness = scheduled_arr - est_arr
#   dep_lateness_str = sec_to_hhmmss(dep_lateness)
#   arr_lateness_str = sec_to_hhmmss(arr_lateness)
#   dep_lateness_class = 'late' if dep_lateness < 0 else ''
#   arr_lateness_class = 'late' if arr_lateness < 0 else ''
#   origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
#   origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
#   destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
#   destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
# else:
#   flight_time_str = "---"
#   actual_time_str = "---"
#   dep_late = 0
#   arr_late = 0
#   actual_time_late = False
#   dep_is_late = False
#   arr_is_late = False
#   flight_time_late = '---'
#   dep_lateness_str = "---"
#   arr_lateness_str = "---"
#   dep_lateness_class = ''
#   arr_lateness_class = ''
#   origin_lat = glom(fr24_detail, 'airport.origin.position.latitude', default=None)
#   origin_lon = glom(fr24_detail, 'airport.origin.position.longitude', default=None)
#   destination_lat = glom(fr24_detail, 'airport.destination.position.latitude', default=None)
#   destination_lon = glom(fr24_detail, 'airport.destination.position.longitude', default=None)
#
# return {
#   "hex_code": hex_code,
#   "registration": registration,
#   "squawk": squawk,
#   "aircraft_type": aircraft_type,
#   "callsign": callsign_str,
#   "airline_icao": airline_icao,
#   "aircraft_code": aircraft_code,
#   "country": aircraft_country,
#   "origin_iata": origin_iata,
#   "origin_city": origin_city,
#   'lat': lat,
#   'lon': lon,
#   'lat_dir': lat_dir,
#   'lon_dir': lon_dir,
#
#   "alt_value": alt_value,
#   "alt_arrow": alt_arrow,
#   "alt_class": alt_class,
#   "gs_value": gs_value,
#   "gs_arrow": gs_arrow,
#   "gs_class": gs_class,
#   "hdg_value": hdg_value,
#   "hdg_arrow": hdg_arrow,
#   "hdg_class": hdg_class,
#
#   "destination_iata": destination_iata,
#   "destination_city": destination_city,
#   "scheduled_dep": scheduled_dep_str,
#   "scheduled_arr": scheduled_arr_str,
#   "actual_dep": actual_dep_str,
#   "est_arr": est_arr_str,
#   "flight_time": flight_time_str,
#   "actual_time": actual_time_str,
#   "dep_late_str": sec_to_hhmmss(abs(dep_late)) if dep_late > 0 else "---",
#   "arr_late_str": sec_to_hhmmss(abs(arr_late)) if arr_late > 0 else "---",
#   "flight_time_late": flight_time_late,
#   "dep_is_late": dep_is_late,
#   "arr_is_late": arr_is_late,
#   "actual_time_late": actual_time_late,
#   "dep_lateness_str": dep_lateness_str,
#   "arr_lateness_str": arr_lateness_str,
#   "dep_lateness_class": dep_lateness_class,
#   "arr_lateness_class": arr_lateness_class,
#   "observed": observed,
# }
