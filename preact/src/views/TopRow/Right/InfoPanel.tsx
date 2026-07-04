import type {
  FlightInfoTopRight,
  RealTimeFlightInfo,
} from "../../../types/FlightInfoRecord.ts";
import Flag from "../../BottomRow/Right/Flag.tsx";
// import { calculateDirection } from "../../utilities/calculateBearing.ts";

const InfoPanel = ({
  topRight,
  realTime,
}: {
  topRight: FlightInfoTopRight;
  realTime: RealTimeFlightInfo;
}) => {
  return (
    <table
      id="info-panel-1"
      class="table-auto border-collapse text-left w-full text-sm"
    >
      <tbody class="divide-y">
        <tr>
          <td>Altitude:</td>
          <td>
            <span>{realTime.alt.toLocaleString()}</span> ft
            <span className={`${realTime.alt_class} pl-2`}>
              {realTime.alt_arrow}
            </span>
          </td>
        </tr>
        <tr>
          <td>Groundspeed:</td>
          <td>
            {realTime.gs === "" ? (
              ""
            ) : (
              <>
                <span>{`${realTime.gs} kts`}</span>
                <span className={`${realTime.gs_class} pl-2`}>
                  {realTime.gs_arrow}
                </span>
              </>
            )}
          </td>
        </tr>
        <tr>
          <td>Heading:</td>
          <td>
            <span>{realTime.hdg}</span> &deg;
            <span className={`${realTime.hdg_class} pl-2`}>
              {realTime.hdg_arrow}
            </span>
          </td>
        </tr>
        <tr>
          <td>Squawk:</td>
          <td id="squawk">
            {realTime.squawk === "" ? "----" : realTime.squawk}
          </td>
        </tr>
        <tr>
          <td>ICAO:</td>
          <td>{topRight.icao ? topRight.icao : ""}</td>
        </tr>
        <tr>
          <td>Registration:</td>
          <td>
            <Flag country={topRight.country.toLowerCase()} />
            <span className="registration pl-1">{topRight.registration}</span>
          </td>
        </tr>
        <tr>
          <td>Position:</td>
          <td id="position">
            <span>{realTime.position}</span>
          </td>
        </tr>
        <tr>
          <td>Aircraft:</td>
          <td id="aircraft">{topRight.aircraft_type}</td>
        </tr>
        <tr>
          <td>Scheduled:</td>
          <td>
            <span>
              {topRight.scheduled[0]} - {topRight.scheduled[1]}
            </span>
          </td>
        </tr>
        <tr>
          <td>Actual/ETA:</td>
          <td>
            <span className={topRight.actual[2] ? "late" : "early"}>
              {topRight.actual[0]}
            </span>
            {" - "}
            <span className={topRight.actual[3] ? "late" : "early"}>
              {topRight.actual[1]}
            </span>
          </td>
        </tr>
        <tr>
          <td>Flight time:</td>
          <td id="flight-time">
            <span>{topRight.flight_time[0]}</span>
            {" - "}
            <span className={topRight.flight_time[2] ? "early" : "late"}>
              {topRight.flight_time[1]}
            </span>
          </td>
        </tr>
        <tr>
          <td>Late/Early:</td>
          <td>TBD</td>
        </tr>
        {/*<tr>*/}
        {/*  <td>Distance:</td>*/}
        {/*  <td id="distance">{dx} mi</td>*/}
        {/*</tr>*/}
        {/*<tr>*/}
        {/*  <td>Bearing:</td>*/}
        {/*  <td id="bearing">*/}
        {/*    {bearing}&deg; {calculateDirection(bearing)}*/}
        {/*  </td>*/}
        {/*</tr>*/}
        {/*<tr>*/}
        {/*  <td>Observed:</td>*/}
        {/*  <td id="observed">{flightInfo.observed}</td>*/}
        {/*</tr>*/}
        {/*<tr>*/}
        {/*  <td colSpan={2} className="text-center">*/}
        {/*    <button*/}
        {/*      className="mt-2 btn btn-sm rounded-lg bg-teal-300 px-4 py-2 text-sm font-medium text-black shadow-sm hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"*/}
        {/*      onClick={openSettings}*/}
        {/*    >*/}
        {/*      Settings*/}
        {/*    </button>*/}
        {/*  </td>*/}
        {/*</tr>*/}
      </tbody>
    </table>
  );
};

export default InfoPanel;
