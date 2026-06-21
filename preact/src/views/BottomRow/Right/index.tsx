import Flag from "./Flag";
import Position from "./Position.tsx";
import DepArrTimes from "./DepArrTimes.tsx";
import EarlyLate from "./EarlyLate.tsx";
import FlyingTime from "./FlyingTime.tsx";
import useFlightData from "../../../hooks/useFlightData.ts";
import {calculateDistance} from "../../utilities/calculateDistance.ts";
import useConfigData from "../../../hooks/useConfigData.ts";
import {
  calculateBearing,
  calculateDirection,
} from "../../utilities/calculateBearing.ts";
import {useState} from "preact/hooks";
import {ViewSettingsModal} from "./ViewSettingsModal.tsx";
import {useAppDispatch, useAppSelector} from "../../../store";
import {setToFlightList} from "../../../store/appSlice.ts";
import ActualTime from "./ActualTime.tsx";

const Right = () => {
  const dispatch = useAppDispatch();
  const {displayRotate, displayRotateInterval} = useAppSelector(state => state.app);
  const [isOpen, setIsOpen] = useState(false);
  const closeSettings = () => setIsOpen(false);
  const openSettings = () => {
    setIsOpen(true);
    dispatch(setToFlightList());
  }

  const {detail, toDisplay} = useFlightData();
  const config = useConfigData();
  const aircraft = detail.aircraft;
  const position = toDisplay.position;
  const observed =
    position[position.length - 1].timestamp - position[0].timestamp;
  const obsMin = Math.floor(observed / 60);
  const obsSec = Math.floor(observed % 60);
  const positionRec = position[position.length - 1];
  const dx = calculateDistance(
    positionRec.latitude,
    positionRec.longitude,
    config.user.home_lat,
    config.user.home_lon,
    "mi",
  )?.toFixed(0);
  const bearing = calculateBearing(
    config.user.home_lat,
    config.user.home_lon,
    positionRec.latitude,
    positionRec.longitude,
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
            <Flag country={aircraft.country.alpha2.toLowerCase()}/>
            <span className="registration pl-1">{aircraft.registration}</span>
          </td>
        </tr>
        <tr>
          <td>Position:</td>
          <td id="position">
            <Position
              lat={positionRec?.latitude}
              lon={positionRec?.longitude}
            />
          </td>
        </tr>
        <tr>
          <td>Aircraft:</td>
          <td id="aircraft">{aircraft?.model.text}</td>
        </tr>
        <tr>
          <td>Flight time:</td>
          <td id="flight-time">
            <FlyingTime/>
          </td>
        </tr>
        <tr>
          <td>Scheduled:</td>
          <td>
            <DepArrTimes
              dep={detail.time.scheduled.departure}
              depTz={detail.airport.origin.timezone.name}
              depTzText={detail.airport.origin.timezone.abbr}
              arr={detail.time.scheduled.arrival}
              arrTz={detail.airport.destination.timezone.name}
              arrTzText={detail.airport.destination.timezone.abbr}
            />
          </td>
        </tr>
        <tr>
          <td>Actual/ETA:</td>
          <td>
            <DepArrTimes
              dep={detail.time.real.departure}
              depTz={detail.airport.origin.timezone.name}
              depTzText={detail.airport.origin.timezone.abbr}
              arr={detail.time.estimated.arrival}
              arrTz={detail.airport.destination.timezone.name}
              arrTzText={detail.airport.destination.timezone.abbr}
              dep0={detail.time.scheduled.departure}
              arr0={detail.time.scheduled.arrival}
            />
          </td>
        </tr>
        <tr>
          <td>Actual time:</td>
          <td><ActualTime/></td>
        </tr>
        <tr>
          <td>Late/Early:</td>
          <td>
            <EarlyLate
              t={detail.time.real.departure}
              t0={detail.time.scheduled.departure}
            />{" "}
            -{" "}
            <EarlyLate
              t={detail.time.estimated.arrival}
              t0={detail.time.scheduled.arrival}
            />
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
          <td id="observed">
            {obsMin}m {obsSec}s
          </td>
        </tr>
        <tr>
          <td colSpan={2} className="text-center">
            <button
              className="mt-2 btn btn-sm rounded-lg bg-teal-300 px-4 py-2 text-sm font-medium text-black shadow-sm hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
              onClick={openSettings}>
              Settings
            </button>
          </td>
        </tr>
        </tbody>
      </table>
      <ViewSettingsModal isOpen={isOpen} onClose={closeSettings} displayRotate={displayRotate}
                         displayRotateInterval={displayRotateInterval}/>
    </div>
  );
};

export default Right;
