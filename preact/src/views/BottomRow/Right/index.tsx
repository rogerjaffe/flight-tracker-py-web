import Flag from "./Flag";
// import Position from "./Position.tsx";
// import DepArrTimes from "./DepArrTimes.tsx";
// import EarlyLate from "./EarlyLate.tsx";
// import FlyingTime from "./FlyingTime.tsx";
import useFlightData from "../../../hooks/useFlightData.ts";
import { calculateDistance } from "../../utilities/calculateDistance.ts";
import useConfigData from "../../../hooks/useConfigData.ts";
import {
  calculateBearing,
  calculateDirection,
} from "../../utilities/calculateBearing.ts";
import { useState } from "preact/hooks";
import { ViewSettingsModal } from "./ViewSettingsModal.tsx";
import { useAppDispatch, useAppSelector } from "../../../store";
import { setToFlightList } from "../../../store/appSlice.ts";
// import ActualTime from "./ActualTime.tsx";

const Right = () => {
  const dispatch = useAppDispatch();
  const { displayRotate, displayRotateInterval } = useAppSelector(
    (state) => state.app,
  );
  const [isOpen, setIsOpen] = useState(false);
  const closeSettings = () => setIsOpen(false);
  const openSettings = () => {
    setIsOpen(true);
    dispatch(setToFlightList());
  };

  const { flightInfo } = useFlightData();
  const { config } = useConfigData();
  const aircraft = flightInfo?.aircraft_type;
  // const position = flightInfo?.lat + " " + flightInfo?.lon;
  // const observed = flightInfo?.observed
  const dx = calculateDistance(
    flightInfo?.lat ?? 0,
    flightInfo?.lon ?? 0,
    config?.user.lat ?? 0,
    config?.user.lon ?? 0,
    "mi",
  )?.toFixed(0);
  const bearing = calculateBearing(
    config?.user.lat ?? 0,
    config?.user.lon ?? 0,
    flightInfo?.lat ?? 0,
    flightInfo?.lon ?? 0,
  );
  if (!aircraft) return null;

  return (
    <div class="col-span-1 mr-1">
      <table
        id="info-panel-2"
        class="table-auto border-collapse w-full text-sm text-left"
      >
        <tbody class="divide-y">
          <tr>
            <td>Registration:</td>
            <td>
              <Flag country={flightInfo.country.toLowerCase()} />
              <span className="registration pl-1">
                {flightInfo.registration}
              </span>
            </td>
          </tr>
          <tr>
            <td>Position:</td>
            <td id="position">
              <span>
                {flightInfo.lat}
                {flightInfo.lat_dir} {flightInfo.lon}
                {flightInfo.lon_dir}
              </span>
            </td>
          </tr>
          <tr>
            <td>Aircraft:</td>
            <td id="aircraft">{flightInfo.aircraft_type}</td>
          </tr>
          <tr>
            <td>Flight time:</td>
            <td id="flight-time">{flightInfo.flight_time}</td>
          </tr>
          <tr>
            <td>Scheduled:</td>
            <td>
              <span>
                {flightInfo.scheduled_dep} - {flightInfo.scheduled_arr}
              </span>
            </td>
          </tr>
          <tr>
            <td>Actual/ETA:</td>
            <td>
              <span>
                {flightInfo.actual_dep} - {flightInfo.est_arr}
              </span>
            </td>
          </tr>
          <tr>
            <td>Actual time:</td>
            <td>
              <span>{flightInfo.actual_time}</span>
            </td>
          </tr>
          <tr>
            <td>Late/Early:</td>
            <td>
              <span className={flightInfo.dep_lateness_class}>
                {flightInfo.dep_lateness_str}
              </span>
              -{" "}
              <span className={flightInfo.arr_lateness_class}>
                {flightInfo.arr_lateness_str}
              </span>
            </td>
          </tr>
          <tr>
            <td>Distance:</td>
            <td id="distance">{dx} mi</td>
          </tr>
          <tr>
            <td>Bearing:</td>
            <td id="bearing">
              {bearing}&deg; {calculateDirection(bearing)}
            </td>
          </tr>
          <tr>
            <td>Observed:</td>
            <td id="observed">{flightInfo.observed}</td>
          </tr>
          <tr>
            <td colSpan={2} className="text-center">
              <button
                className="mt-2 btn btn-sm rounded-lg bg-teal-300 px-4 py-2 text-sm font-medium text-black shadow-sm hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
                onClick={openSettings}
              >
                Settings
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <ViewSettingsModal
        isOpen={isOpen}
        onClose={closeSettings}
        displayRotate={displayRotate}
        displayRotateInterval={displayRotateInterval}
      />
    </div>
  );
};

export default Right;
