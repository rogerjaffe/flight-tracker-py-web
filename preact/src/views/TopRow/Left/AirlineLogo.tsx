import fallbackImg from "../../../assets/airplane.png";
import useFlightData from "../../../hooks/useFlightData.ts";
import useConfigData from "../../../hooks/useConfigData.ts";

const AirlineLogo = () => {
  const { toDisplay } = useFlightData();
  const config = useConfigData();
  const airlineIcao = toDisplay.flight.airline_icao || "Unknown";
  return (
    <img
      id="airline-logo"
      src={`${config.app.airline_logo_url}${airlineIcao}${config.app.airline_logo_url_ext}`}
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
