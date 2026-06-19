/**
 * Calculates the bearing in degrees between two geographic points.
 * @param {number} lat1 Latitude of the start point in decimal degrees.
 * @param {number} lon1 Longitude of the start point in decimal degrees.
 * @param {number} lat2 Latitude of the end point in decimal degrees.
 * @param {number} lon2 Longitude of the end point in decimal degrees.
 * @returns {number} The bearing in degrees, ranging from 0 to 360 (clockwise from North).
 */
export const calculateBearing = (
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
) => {
  // Convert degrees to radians
  const toRadians = (deg: number) => (deg * Math.PI) / 180;
  const toDegrees = (rad: number) => (rad * 180) / Math.PI;

  const phi1 = toRadians(lat1);
  const phi2 = toRadians(lat2);
  const deltaLon = toRadians(lon2 - lon1);

  // Calculate components for atan2
  const y = Math.sin(deltaLon) * Math.cos(phi2);
  const x =
    Math.cos(phi1) * Math.sin(phi2) -
    Math.sin(phi1) * Math.cos(phi2) * Math.cos(deltaLon);

  // Use Math.atan2 to get the bearing in radians, then convert to degrees
  let bearing = Math.atan2(y, x);
  bearing = toDegrees(bearing);

  // Normalize the bearing to a 0-360 degree range (clockwise from North)
  return (bearing + 360) % 360;
};

export const calculateDirection = (bearing: number) => {
  const directions = [
    { s: 0, e: 11.25, d: "N" },
    { s: 11.25, e: 33.75, d: "NNE" },
    { s: 33.75, e: 56.25, d: "NE" },
    { s: 56.25, e: 78.75, d: "ENE" },
    { s: 78.75, e: 101.25, d: "E" },
    { s: 101.25, e: 123.75, d: "ESE" },
    { s: 123.75, e: 146.25, d: "SE" },
    { s: 146.25, e: 168.75, d: "SSE" },
    { s: 168.75, e: 191.25, d: "S" },
    { s: 191.25, e: 213.75, d: "SSW" },
    { s: 213.75, e: 236.25, d: "SW" },
    { s: 236.25, e: 258.75, d: "WSW" },
    { s: 258.75, e: 281.25, d: "W" },
    { s: 281.25, e: 303.75, d: "WNW" },
    { s: 303.75, e: 326.25, d: "NW" },
    { s: 326.25, e: 348.75, d: "NNW" },
    { s: 348.75, e: 360, d: "N" },
  ];
  const rec = directions.find(({ s, e }) => s <= bearing && bearing < e);
  return rec ? rec.d : "";
};
