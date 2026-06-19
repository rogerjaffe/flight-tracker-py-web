import Map from "./Map";
import Distance from "./Distance.tsx";
import FlightList from "./FlightList.tsx";
import {useAppSelector} from "../../../store";

const Left = () => {
  const {displayContent} = useAppSelector((state) => state.app);

  if (displayContent === "map") {
    return (
      <div class="col-span-3 border-black border-r">
        <Map/>
      </div>
    );
  } else if (displayContent === "distance") {
    return (
      <div class="col-span-3 border-black border-r overflow-y-auto">
        <Distance/>
      </div>
    );
  } else if (displayContent === "flight") {
    return (
      <div class="col-span-3 border-black border-r overflow-y-auto">
        <FlightList/>
      </div>
    );
  }
};
export default Left;
