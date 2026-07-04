import { briefAirlineName } from "../../utilities/briefAirlineName.ts";
import useConfigData from "../../../hooks/useConfigData.ts";
import type { FlightInfoTopRight } from "../../../types/FlightInfoRecord.ts";

const FlightText = ({ topRight }: { topRight: FlightInfoTopRight }) => {
  const { config } = useConfigData();
  const max_airline_name_length = config?.app.max_airline_name_length || 15;
  const airlineName = briefAirlineName(
    topRight.airline_text || "Unknown",
  ).substring(0, max_airline_name_length);
  const number = topRight.flight_number;
  const flightText = `${airlineName} ${number}`;
  const font = airlineName.length < 15 ? "text-xl" : "text-sm";
  return (
    <div id="full-flight-text" class="text-2xl font-bold text-center">
      <span class={font}>{flightText}</span>
    </div>
  );
};

export default FlightText;
