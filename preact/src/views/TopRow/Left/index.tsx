import AirlineLogo from "./AirlineLogo.tsx";
import FlightIcao from "./FlightIcao.tsx";
import AircraftCode from "./AircraftCode.tsx";
import { useAppSelector } from "../../../store";

const LeftSide = () => {
  const { top_left } = useAppSelector((state) => state.flightInfo);
  return (
    <div className="col-span-1 row-start-1 border-black border-r border-b-2">
      <AirlineLogo topLeft={top_left} />
      <FlightIcao topLeft={top_left} />
      <AircraftCode topLeft={top_left} />
    </div>
  );
};

export default LeftSide;
