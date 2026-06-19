import AirlineLogo from "./AirlineLogo.tsx";
import FlightIcao from "./FlightIcao.tsx";
import AircraftCode from "./AircraftCode.tsx";

const LeftSide = () => {
  return (
    <div className="col-span-2 border-black border-r">
      <AirlineLogo />
      <FlightIcao />
      <AircraftCode />
    </div>
  );
};

export default LeftSide;
