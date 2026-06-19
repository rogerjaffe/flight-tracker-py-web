import OriginDestination from "./OriginDestination.tsx";
import ProgressBar from "./ProgressBar.tsx";
import {useAppDispatch} from "../../../store";
import {toggleDisplay} from "../../../store/appSlice.ts";
import ArrowRight from "../../utilities/ArrowRight.tsx";

const Middle = () => {
  const dispatch = useAppDispatch();

  const switchView = () => {
    dispatch(toggleDisplay());
  };

  return (
    <div className="col-span-9">
      <div className="grid grid-cols-7 gap-1 text-center">
        <div className="col-span-3">
          <OriginDestination isOrigin={true}/>
        </div>
        <div className="col-span-1 cursor-pointer" onClick={switchView}>
          <ArrowRight size={96}/>
        </div>
        <div className="col-span-3">
          <OriginDestination isOrigin={false}/>
        </div>
      </div>
      <ProgressBar/>
    </div>
  );
};

export default Middle;
