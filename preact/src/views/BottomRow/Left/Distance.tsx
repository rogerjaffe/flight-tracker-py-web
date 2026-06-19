import NumberWithArrow from "../../utilities/NumberWithArrow.tsx";
import useFlightData from "../../../hooks/useFlightData.ts";
import {calculateDistance} from "../../utilities/calculateDistance.ts";
import useConfigData from "../../../hooks/useConfigData.ts";
import {calculateBearing, calculateDirection} from "../../utilities/calculateBearing.ts";

const Distance = () => {
  const {flightList, detail} = useFlightData();

  if (!flightList) return null;
  const thisAcHex = detail?.aircraft?.hex ?? "";
  const {user} = useConfigData()
  const {home_lat, home_lon} = user;
  const flightObjs = Object.values(flightList);
  const flightData = flightObjs.map((flightObj) => {
    const lastPosition = flightObj.position[flightObj.position.length - 1];
    const dx = calculateDistance(home_lat, home_lon, lastPosition.latitude, lastPosition.longitude, 'mi') ?? 0;
    const bearing = calculateBearing(home_lat, home_lon, lastPosition.latitude, lastPosition.longitude) ?? -1;
    const direction = bearing === -1 ? '' : calculateDirection(bearing);
    return {
      hex: flightObj.flight.hex,
      callsign: flightObj.flight.callsign,
      position: flightObj.position,
      origin: flightObj.flight.origin_airport_iata,
      destination: flightObj.flight.destination_airport_iata,
      dx,
      bearing,
      direction,
    };
  })

  flightData.sort((a, b) => (a.dx - b.dx));
  const half = Math.ceil(flightData.length / 2);
  const leftGroup = flightData.slice(0, half);
  const rightGroup = flightData.slice(half);

  if (!flightList || !detail) {
    return <div className="h-full text-center">Loading...</div>;
  } else {
    return (
      <table
        id="distance-list"
        class="table-auto border-collapse w-full text-left text-xs min-w-full"
      >
        <thead class="sticky top-0 bg-gray-50 shadow-sm  [&_th]:pl-2 [&_th]:pr-2">
        <tr class="border-black border-b-2">
          <th className="text-center">Flight</th>
          <th className="text-center">From/To</th>
          <th className="text-center">Dx</th>
          <th className="text-center">Direction</th>
          <th className="text-center">Altitude</th>
          <th className="text-center">Flight</th>
          <th className="text-center">From/To</th>
          <th className="text-center">Dx</th>
          <th className="text-center">Direction</th>
          <th className="text-center">Altitude</th>
        </tr>
        </thead>
        <tbody className="divide-y [&_td]:pl-2 [&_td]:pr-2">
        {leftGroup.map((leftItem, index) => {
          const rightItem = rightGroup[index];
          const rightHex = rightItem?.hex ?? "none";
          const leftHex = leftItem.hex;
          const rightClass = rightHex === thisAcHex ? "bg-yellow-300" : "";
          const leftClass = leftHex === thisAcHex ? "bg-yellow-300" : "";
          const col1AltitudeText = NumberWithArrow({
            position: leftItem.position,
            prop: "altitude",
            units: "ft",
            direction: "ud",
          });

          const col2AltitudeText = rightItem
            ? NumberWithArrow({
              position: rightItem.position,
              prop: "altitude",
              units: "ft",
              direction: "ud",
            })
            : "";

          return (
            <tr key={leftItem.hex}>
              <td className={`text-center ${leftClass}`}>{leftItem.callsign}</td>
              <td className={leftClass}>
                {leftItem.origin}
                {" - "}
                {leftItem.destination}
              </td>
              <td className={`text-center ${leftClass}`}>{leftItem.dx.toFixed(0)} mi</td>
              <td className={`text-center ${leftClass}`} style={{paddingRight: "2px"}}>
                {leftItem.bearing}&deg;{" "}
                {leftItem.direction}
              </td>
              <td className={`text-right ${leftClass}`}>{col1AltitudeText}</td>
              <td className={`text-center ${rightClass}`}>{rightItem ? rightItem.callsign : ""}</td>
              <td className={rightClass}>
                {
                  rightItem ? (<span>{rightItem.origin} - {rightItem.destination}</span>
                  ) : ""
                }
              </td>
              <td className={`text-center ${rightClass}`}>{rightItem ? `${rightItem.dx.toFixed(0)} mi` : ""}</td>
              <td className={`text-center ${rightClass}`}>
                {rightItem ? <span>{rightItem.bearing}&deg;{" "}{rightItem.direction}</span> : ""}
              </td>
              <td className={`text-right ${rightClass}`}>{col2AltitudeText}</td>
            </tr>
          );
        })}
        </tbody>
      </table>
    );
  }


  // return (
  //   <table
  //     id="distance-list"
  //     class="table-auto border-collapse w-full text-left text-sm min-w-full"
  //   >
  //     <thead class="sticky top-0 bg-gray-50 shadow-sm  [&_th]:pl-2 [&_th]:pr-2">
  //     <tr class="border-black border-b-2">
  //       <th>Flight</th>
  //       <th>From/To</th>
  //       <th>Dx</th>
  //       <th>Dir</th>
  //       <th>Altitude</th>
  //       <th>Flight</th>
  //       <th>From/To</th>
  //       <th>Dx</th>
  //       <th>Dir</th>
  //       <th>Altitude</th>
  //     </tr>
  //     </thead>
  //     <tbody class="divide-y [&_td]:pl-2 [&_td]:pr-2">
  //     <tr>
  //       <td>ASA4</td>
  //       <td>SAN-HLO</td>
  //       <td>53nm</td>
  //       <td>243&deg; SSW</td>
  //       <td>27,000ft</td>
  //       <td>SWA892</td>
  //       <td>LAX-TUC</td>
  //       <td>82nm</td>
  //       <td>8&deg; N</td>
  //       <td>8,500ft</td>
  //     </tr>
  //     </tbody>
  //   </table>
  // );
};

export default Distance;
