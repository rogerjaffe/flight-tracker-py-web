import json
from curl_cffi import requests


class Airline:
  def __init__(self):
    self.airline_list = []
    self.url = "https://openflights.org/php/alsearch.php"

  def get_iata(self, icao_code):
    iata = self.is_in_list(icao_code)
    if iata:
      return iata
    else:
      payload = {
        "name": "",
        "alias": "",
        "iata": "",
        "callsign": "",
        "active": "",
        "alid": "",
        "icao": icao_code,
        "action": "SEARCH",
        "country": "ALL",
        "mode": "F",
        "offset": 0,
        "iatafilter": True
      }
      response = requests.post(url=self.url, data=payload)
      response_list = response.text.split("\n")
      json_body = json.loads(response_list[1])
      iata = json_body['iata']
      name = json_body['name']
      callsign = json_body['callsign']
      self.airline_list.append({'icao': icao_code, 'iata': iata, 'name': name, 'callsign': callsign})
      return iata

  def is_in_list(self, icao_code):
    for airline in self.airline_list:
      if airline['icao'] == icao_code:
        return airline['iata']
    return None
