import Map from "./Map";
import Distance from "./Distance.tsx";
import FlightList from "./FlightList.tsx";
import {useAppDispatch, useAppSelector} from "../../../store";
import {useInterval} from "../../../hooks/useInterval.ts";
import {toggleDisplay} from "../../../store/appSlice.ts";
import Version from "./Version.tsx";

const Left = () => {
  const {displayContent, displayRotateInterval, displayRotate} = useAppSelector((state) => state.app);
  const dispatch = useAppDispatch();

  const nextView = () => {
    if (displayRotate) {
      dispatch(toggleDisplay());
    }
  }

  useInterval(nextView, displayRotateInterval * 1000)

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
        <Version/>
      </div>
    );
  } else if (displayContent === "flight") {
    return (
      <div class="col-span-3 border-black border-r overflow-y-auto">
        <FlightList/>
        <Version/>
      </div>
    );
  }
};
export default Left;
