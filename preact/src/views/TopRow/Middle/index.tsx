import OriginDestination from "./OriginDestination.tsx";
import ProgressBar from "./ProgressBar.tsx";
import { useAppDispatch, useAppSelector } from "../../../store";
import { toggleDisplay } from "../../../store/appSlice.ts";
import ArrowRight from "../../utilities/ArrowRight.tsx";

const Middle = () => {
  const { top_middle, real_time } = useAppSelector((state) => state.flightInfo);
  const dispatch = useAppDispatch();

  const switchView = () => {
    dispatch(toggleDisplay());
  };

  return (
    <div className="col-span-5 row-start-1 border-black border-b-2">
      <div className="grid grid-cols-7 gap-1 text-center">
        <div className="col-span-3">
          <OriginDestination
            realTime={real_time}
            topMiddle={top_middle}
            isOrigin={true}
          />
        </div>
        <div className="col-span-1 cursor-pointer" onClick={switchView}>
          <ArrowRight size={96} />
        </div>
        <div className="col-span-3">
          <OriginDestination
            realTime={real_time}
            topMiddle={top_middle}
            isOrigin={false}
          />
        </div>
      </div>
      <ProgressBar realTime={real_time} />
    </div>
  );
};

export default Middle;
