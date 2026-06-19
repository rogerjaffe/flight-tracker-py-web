type Units = "nm" | "mi" | "m" | "km";

const METERS_TO_KM = 0.001;
const METERS_TO_MI = 0.000621371;
const METERS_TO_NM = 0.000539957;

export const calculateDistance = (
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
  units: Units,
) => {
  const R = 6371e3; // Earth's radius in meters
  const phi1 = (lat1 * Math.PI) / 180; // convert to radians
  const phi2 = (lat2 * Math.PI) / 180;
  const deltaPhi = ((lat2 - lat1) * Math.PI) / 180;
  const deltaGamma = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
    Math.cos(phi1) *
      Math.cos(phi2) *
      Math.sin(deltaGamma / 2) *
      Math.sin(deltaGamma / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  const meters = R * c; // Distance in meters
  switch (units) {
    case "m":
      return meters;
    case "km":
      return meters * METERS_TO_KM;
    case "mi":
      return meters * METERS_TO_MI;
    case "nm":
      return meters * METERS_TO_NM;
    default:
      return null;
  }
};
