import useFlightData from "../../../hooks/useFlightData.ts";

const FlightIcao = () => {
  const { toDisplay } = useFlightData();
  const airlineIcao = toDisplay.flight.callsign?.substring(0, 3) ?? "Unknown";
  const flightNumber = toDisplay.flight.callsign?.substring(3) ?? "";

  return (
    <div id="icao-flight" className="text-xl font-bold">
      {airlineIcao} {flightNumber}
    </div>
  );
};

export default FlightIcao;
