import {type TargetedMouseEvent} from "preact";
import NumberWithArrow from "../../utilities/NumberWithArrow.tsx";
import useFlightData from "../../../hooks/useFlightData.ts";
import {setFlight} from "../../../bridge/pythonBridge";

const FlightList = () => {
  const {flightList, detail} = useFlightData();

  const gotoHex = (e: TargetedMouseEvent<HTMLTableCellElement>) => {
    const hexCode = e.currentTarget.getAttribute('data-hex');
    if (!hexCode) return;
    setFlight(hexCode);
  }

  if (!flightList) return null;
  const flightObjs = Object.values(flightList);
  const thisAcHex = detail?.aircraft?.hex ?? "";
  flightObjs.sort((a, b) => (a.flight.callsign < b.flight.callsign ? -1 : 1));
  const half = Math.ceil(flightObjs.length / 2);
  const leftGroup = flightObjs.slice(0, half);
  const rightGroup = flightObjs.slice(half);

  if (!flightList || !detail) {
    return <div className="h-full text-center">Loading...</div>;
  } else {
    return (
      <table
        id="flight-list"
        class="table-auto border-collapse w-full text-left text-sm min-w-full"
      >
        <thead class="sticky top-0 bg-gray-50 shadow-sm [&_th]:pl-2 [&_th]:pr-2">
        <tr class="border-black border-b-2 text-left">
          <th>
            <span>Flight</span>
          </th>
          <th>
            <span>From / To</span>
          </th>
          <th className="text-center">
            <span>Altitude</span>
          </th>
          <th className="text-center">
            <span>Speed</span>
          </th>
          <th>
            <span>Flight</span>
          </th>
          <th>
            <span>From / To</span>
          </th>
          <th className="text-center">
            <span>Altitude</span>
          </th>
          <th className="text-center">
            <span>Speed</span>
          </th>
        </tr>
        </thead>
        <tbody className="divide-y [&_td]:pl-2 [&_td]:pr-2">
        {leftGroup.map((leftItem, index) => {
          const rightItem = rightGroup[index];
          const rightHex = rightItem?.flight.hex ?? "none";
          const leftHex = leftItem.flight.hex;
          const rightClass = rightHex === thisAcHex ? "bg-yellow-300" : "";
          const leftClass = leftHex === thisAcHex ? "bg-yellow-300" : "";
          const col1AltitudeText = NumberWithArrow({
            position: leftItem.position,
            prop: "altitude",
            units: "ft",
            direction: "ud",
          });
          const col1SpeedText = NumberWithArrow({
            position: leftItem.position,
            prop: "ground_speed",
            units: "kts",
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
          const col2SpeedText = rightItem
            ? NumberWithArrow({
              position: rightItem.position,
              prop: "ground_speed",
              units: "kts",
              direction: "ud",
            })
            : "";

          return (
            <tr key={leftItem.flight.hex} className="cursor-pointer">
              <td className={leftClass} data-hex={leftItem.hex} onClick={gotoHex}>{leftItem.flight.callsign}</td>
              <td className={leftClass} data-hex={leftItem.hex} onClick={gotoHex}>
                {leftItem.flight.origin_airport_iata}
                {" - "}
                {leftItem.flight.destination_airport_iata}
              </td>
              <td className={`text-right ${leftClass}`} data-hex={leftItem.hex} onClick={gotoHex}>
                {col1AltitudeText}
              </td>
              <td className={`text-right ${leftClass}`} data-hex={leftItem.hex} onClick={gotoHex}>{col1SpeedText}</td>
              <td className={rightClass} data-hex={rightItem?.hex ?? ''} onClick={gotoHex}>
                {rightItem?.flight.callsign || ""}
              </td>
              <td className={rightClass} data-hex={rightItem?.hex ?? ''} onClick={gotoHex}>
                {rightItem?.flight.origin_airport_iata || ""}
                {rightItem ? " - " : ""}
                {rightItem?.flight.destination_airport_iata || ""}
              </td>
              <td className={`text-right ${rightClass}`} data-hex={rightItem?.hex ?? ''} onClick={gotoHex}>
                {rightItem ? col2AltitudeText : ""}
              </td>
              <td className={`text-right ${rightClass}`} data-hex={rightItem?.hex ?? ''}
                  onClick={gotoHex}>{col2SpeedText}</td>
            </tr>
          );
        })}
        </tbody>
      </table>
    );
  }
};

export default FlightList;
