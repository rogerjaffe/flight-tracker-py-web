import useFlightData from "../../../hooks/useFlightData.ts";

const AircraftCode = () => {
  const { toDisplay } = useFlightData();

  const aircraftCode = toDisplay.flight.aircraft_code || "Unknown";
  return (
    <div id="icao-flight" className="text-sm">
      {aircraftCode}
    </div>
  );
};

export default AircraftCode;
