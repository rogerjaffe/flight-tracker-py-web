from typing import Any
from glom import glom
from utilities import get_value_arrow_class, http_request
from data_types.fr24_flight_detail import Fr24FlightDetail


def lookup_reg_from_hex(hex_code):
  url = f"https://api.airplanes.live/v2/hex/{hex_code}"
  res = http_request(url, 'GET')
  ac_list = res.get('ac', None)
  if ac_list is not None:
    if len(ac_list) == 0:
      raise Exception("ACListIsEmpty")
    else:
      reg = ac_list[0].get('r', None)
      if reg is None:
        raise Exception("RegNotFound")
      else:
        return reg
  else:
    raise Exception("NoACList")

    # val.reg = reg
    # self.lookup_detail(val)

  # self.status_counts()
  # self.timer.singleShot(self.config.app.airplanes_live_reg_interval * 1000, self.lookup_reg_from_hex)


########################################################
# Aircraft detail lookup from registration reducer
########################################################
def lookup_detail(reg) -> Any:
  url = f"https://api.flightradar24.com/common/v1/flight/list.json?&fetchBy=reg&page=1&limit=25&query={reg}"
  res = http_request(url, 'GET')
  data = glom(res, 'result.response.data', default=None)
  if data is None:
    raise Exception("NoData")
  else:
    live_flight = next((x for x in data if glom(x, 'status.live', default=False)), None)
    if live_flight is None:
      raise Exception("NoLiveFlight")
    else:
      assert isinstance(live_flight, dict)
      fr24_flight_detail = Fr24FlightDetail(**live_flight)
      return fr24_flight_detail


def get_list_detail(hex_code, fr24_flight_detail, adsb):
  callsign = glom(fr24_flight_detail, 'identification.callsign', default="")
  origin = glom(fr24_flight_detail, 'airport.origin.code.iata', default="")
  dest = glom(fr24_flight_detail, 'airport.destination.code.iata', default="")
  alt, alt_arrow, alt_class = get_value_arrow_class(adsb, 'alt_baro', 'ud')
  gs, gs_arrow, gs_class = get_value_arrow_class(adsb, 'gs', 'lr')
  rec = {
    'callsign': callsign,
    'origin': origin,
    'dest': dest,
    'alt': alt,
    'alt_arrow': alt_arrow,
    'alt_class': alt_class,
    'gs': gs,
    'gs_arrow': gs_arrow,
    'gs_class': gs_class,
    'hex_code': hex_code,
  }
  return rec


def update_flight_list_detail(flight_list_item):
  adsb = flight_list_item.adsb
  ui_list = flight_list_item.ui_list
  if adsb is None or ui_list is None:
    return flight_list_item
  alt, alt_arrow, alt_class = get_value_arrow_class(adsb, 'alt_baro', 'ud')
  gs, gs_arrow, gs_class = get_value_arrow_class(adsb, 'gs', 'lr')
  rec = {
    'alt': alt,
    'alt_arrow': alt_arrow,
    'alt_class': alt_class,
    'gs': gs,
    'gs_arrow': gs_arrow,
    'gs_class': gs_class,
  }
  ui_list = ui_list | rec
  return ui_list

# def get_ui_regions_static_detail(fr24_detail: Fr24FlightDetail) -> UIStaticFlightDetails:
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
#     "squawk": "1234",
#     "icao": "AABBCC",
#     "registration": "N90823",
#     "position": "32.5643N 117.2234W",
#     "aircraft_type": "B738",
#     "flight_time": "5h 23m",
#     "scheduled": ("14:33", "PDT", "22:45", "CET"),  # dep_time, dep_tz_abbr, arr_time, arr_tz_abbr
#     "actual_eta": ("14:35", "PDT", "20:11", "CET", False, True),  # act, act_tz, eta, eta_tz, is_act_late, is_eta_late
#     "deviation": ("4m 25s", "2m 54s", True, False),  # act, eta, is_act_late, is_eta_late
#   }
#
#   return {
#     "top_left": top_left,
#     "top_middle": top_middle,
#     "top_right": top_right
#   }
#
#
# def get_real_time_detail(flight):
#   return {
#     "altitude": (12000, 'ft', "▲", 'inc'),
#     "groundspeed": (245, 'kts', "▼", 'inc'),
#     "heading": (132, "\u00B0", "◀", 'dec'),
#     "distance": (23, "mi"),  # distance, units
#     "bearing": (239, "WSW"),  # bearing, compass
#     "observed": "27m 12s"
#   }
