NOTES:
pip install "pandas<2.0.0" otherwise traffic.data throws an error

Airline icao / iata lookup -- see API at https://openflights.org/php/alsearch.php
Search page at https://openflights.org/html/alsearch

Now I can just convert icao => iata airline code and lookup the flight on FR24 instead of finding the registration from
the hex code

Flags courtesy of https://www.npmjs.com/package/flag-icons

Production:
sqlite3 should be ":memory:"

0. Revise backend to include backend only state, then state that is shared with the frontend.
   See https://share.google/aimode/4huIoIyIt9M6ZzvDc, option 1.
   a. selected flight
   b. adsb for flight
   c. brief flight info
   d. system status.
   e. configuration

1. Add unit tests for backend!!

Use the FlightRadar24API free version -- see sample code in
adsb-tracker-db-template/references/plane-tracker-rgb-pi-main/js/index.js to get a list of planes in the radius. Still
need to run a server to use the library

Perhaps look at a Python app with display interface to avoid CORS issues with a website?
See https://share.google/aimode/Iw9DBgQl2sRonakAz for reactive Python like React

API for basic information flight lookup from FR24. This is what they use for the search bar
https://www.flightradar24.com/v1/search/web/find?query=fft4964&limit=50

const dx = useMemo(() => {
if (!home_lat || !home_lon) return "";
if (!toDisplay || toDisplay.position.length === 0) return "";
const position = toDisplay?.position[toDisplay?.position.length - 1];
const { latitude, longitude } = position;
return calculateDistance(home_lat, home_lon, latitude, longitude, "nm");
}, [home_lat, home_lon, toDisplay]);

Settings | Display to turn off virtual keyboard
pip freeze > requirements.txt

git clone
cd into project folder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

to start, navigate to the project folder and run:
PYTHONUNBUFFERED=1 QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --disable-software-rasterizer" python .

These kiosk-mode autostart instructions are for R-Pi Trixie OS:

In start_kiosk.sh:

```bash
#!/bin/bash
# If there is a problem with the EGL driver use the following command
# to identify the display name
#
# ls -la /run/user/1000/wayland-* to see the display name
#
# then change the export WAYLAND_DISPLAY= line below to match
# Wait briefly for Trixie's graphics socket to settle on boot

sleep 5

# Define the Wayland Display requirements

export XDG_RUNTIME_DIR=/run/user/$(id -u)
export WAYLAND_DISPLAY=wayland-0 # Adjust this if your display name is different
export QT_QPA_PLATFORM=wayland

# Fix the EGL driver for the Raspberry Pi 3B+

export QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --disable-software-rasterizer"

# Navigate to your .venv project folder and start the app
# Note: Your folder may be different than /home/pi. Check
# the path if there's a problem starting the application.
cd /home/pi/flight-tracker-py-web
source .venv/bin/activate
python .
```