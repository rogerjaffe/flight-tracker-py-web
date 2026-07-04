import FlightText from "./FlightText.tsx";
import InfoPanel from "./InfoPanel.tsx";
import { useAppSelector } from "../../../store";

const Right = () => {
  const { top_right, real_time } = useAppSelector((state) => state.flightInfo);
  return (
    <div class="col-span-2 row-start-1 row-span-5 border-black border-l border-b-2 pl-2 pr-1">
      <FlightText topRight={top_right} />
      <InfoPanel topRight={top_right} realTime={real_time} />
    </div>
  );
};

export default Right;
