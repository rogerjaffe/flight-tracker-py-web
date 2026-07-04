import type { FlightInfoTopLeft } from "../../../types/FlightInfoRecord.ts";

const AircraftCode = ({ topLeft }: { topLeft: FlightInfoTopLeft }) => {
  return (
    <div id="icao-flight" className="text-sm text-center">
      {topLeft?.aircraft_code ?? ""}
    </div>
  );
};

export default AircraftCode;
