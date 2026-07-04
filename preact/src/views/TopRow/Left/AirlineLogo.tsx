import fallbackImg from "../../../assets/airplane.png";
// import useFlightData from "../../../hooks/useFlightData.ts";
import useConfigData from "../../../hooks/useConfigData.ts";
import type { FlightInfoTopLeft } from "../../../types/FlightInfoRecord.ts";

const AirlineLogo = ({ topLeft }: { topLeft: FlightInfoTopLeft }) => {
  const { config } = useConfigData();
  const airlineIcao = topLeft?.airline_icao ?? "";
  const url = config?.app.airline_logo_url ?? "";
  const ext = config?.app.airline_logo_url_ext ?? "";
  return (
    <img
      id="airline-logo"
      src={`${url}${airlineIcao}${ext}`}
      alt="AirlineIcon"
      className="airline-logo p-2"
      onError={(e) => {
        e.currentTarget.onerror = null;
        e.currentTarget.src = fallbackImg;
      }}
    />
  );
};

export default AirlineLogo;
