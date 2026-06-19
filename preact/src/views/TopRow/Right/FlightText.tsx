import { briefAirlineName } from "../../utilities/briefAirlineName.ts";
import useFlightData from "../../../hooks/useFlightData.ts";
import useConfigData from "../../../hooks/useConfigData.ts";

const FlightText = () => {
  const { detail } = useFlightData();
  const config = useConfigData();
  const max_airline_name_length = config.max_airline_name_length || 15;
  const airlineName = briefAirlineName(
    detail.airline.name || "Unknown",
  ).substring(0, max_airline_name_length);
  const number = detail.identification.callsign.substring(3) || "";
  const flightText = `${airlineName} ${number}`;
  const font = airlineName.length < 15 ? "text-xl" : "text-sm";
  return (
    <div id="full-flight-text" class="text-2xl font-bold">
      <span class={font}>{flightText}</span>
    </div>
  );
};

export default FlightText;
