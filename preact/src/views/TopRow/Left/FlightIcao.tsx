import type { FlightInfoTopLeft } from "../../../types/FlightInfoRecord.ts";

const FlightIcao = ({ topLeft }: { topLeft: FlightInfoTopLeft }) => {
  return (
    <div id="icao-flight" className="text-xl text-center font-bold">
      {topLeft.callsign}
    </div>
  );
};

export default FlightIcao;
