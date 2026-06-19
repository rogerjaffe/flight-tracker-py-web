import type { FlightRecord } from "../../types/BackendFlightPayload.ts";

const findDirection = (direction: "ud" | "lr", flightObj: FlightRecord) => {
  if (!flightObj || flightObj.position.length < 2) return "";
  const first = flightObj.position[flightObj.position.length - 2].altitude;
  const second = flightObj.position[flightObj.position.length - 1].altitude;
  if (direction === "ud") {
    return second - first > 0 ? "up" : "down";
  } else {
    return second - first > 0 ? "right" : "left";
  }
};

export default findDirection;
