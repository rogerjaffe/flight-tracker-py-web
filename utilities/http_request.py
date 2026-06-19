from typing import Literal
from curl_cffi import requests


def http_request(url: str, method: Literal["GET", "POST", "PUT", "DELETE"] = "GET"):
  try:
    response = requests.request(method=method, url=url, timeout=10, impersonate='chrome146')

    # 1. Verify success (raises exception for 4xx or 5xx codes)
    response.raise_for_status()

    # 2. Extract JSON data
    data = response.json()

    # 3. Verify data is returned (truthiness check)
    if data:
      return data
    else:
      print("Request successful, but returned empty data.")
      return None

  except Exception as err:
    print(f"HTTPRequest: {err}")
    return None
