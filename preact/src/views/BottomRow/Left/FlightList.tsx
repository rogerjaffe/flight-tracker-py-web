import { type TargetedMouseEvent } from "preact";
// import NumberWithArrow from "../../utilities/NumberWithArrow.tsx";
// import useFlightData from "../../../hooks/useFlightData.ts";
import { setFlight } from "../../../bridge/pythonBridge";
import { useAppSelector } from "../../../store";

const FlightList = () => {
  const { flightList: flightListObj } = useAppSelector(
    (state) => state.flightList,
  );
  const { top_right } = useAppSelector((state) => state.flightInfo);

  const gotoHex = (e: TargetedMouseEvent<HTMLTableCellElement>) => {
    const hexCode = e.currentTarget.getAttribute("data-hex");
    if (!hexCode) return;
    setFlight(hexCode);
  };

  if (!flightListObj) return null;
  const flightList = Object.values(flightListObj);
  const sortedFlightList = flightList.toSorted((a, b) =>
    a.callsign < b.callsign ? -1 : 1,
  );
  const hexCode = top_right?.icao ?? "";
  // const flightInfo = sortedFlightList.find(
  //   (flight) => flight.hex_code === flightList.hex_code,
  // );
  // const flightObjs = Object.values(flightList);
  // const thisAcHex = flightInfo?.hex_code ?? "";
  // flightObjs.sort((a, b) => (a.callsign < b.callsign ? -1 : 1));
  const half = Math.ceil(sortedFlightList.length / 2);
  const leftGroup = sortedFlightList.slice(0, half);
  const rightGroup = sortedFlightList.slice(half);

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
          const rightHex = rightItem?.hex_code ?? "none";
          const leftHex = leftItem.hex_code;
          const rightClass = rightHex === hexCode ? "bg-yellow-300" : "";
          const leftClass = leftHex === hexCode ? "bg-yellow-300" : "";

          return (
            <tr key={leftItem.hex_code} className="cursor-pointer">
              <td
                className={leftClass}
                data-hex={leftItem.hex_code}
                onClick={gotoHex}
              >
                {leftItem.callsign}
              </td>
              <td
                className={leftClass}
                data-hex={leftItem.hex_code}
                onClick={gotoHex}
              >
                {leftItem.origin}
                {" - "}
                {leftItem.dest}
              </td>
              <td
                className={`text-right ${leftClass}`}
                data-hex={leftItem.hex_code}
                onClick={gotoHex}
              >
                {leftItem ? (
                  <>
                    <span>{leftItem.alt}</span> ft{" "}
                    <span className={`${leftItem.alt_class} arrow-width`}>
                      {leftItem.alt_arrow}
                    </span>
                  </>
                ) : (
                  ""
                )}
              </td>
              <td
                className={`text-right ${leftClass}`}
                data-hex={leftItem.hex_code}
                onClick={gotoHex}
              >
                {leftItem ? (
                  <>
                    <span>{`${leftItem.gs} kts`}</span>{" "}
                    <span className={`${leftItem.gs_class} arrow-width`}>
                      {leftItem.gs_arrow}
                    </span>
                  </>
                ) : (
                  ""
                )}
              </td>
              <td
                className={rightClass}
                data-hex={rightItem?.hex_code ?? ""}
                onClick={gotoHex}
              >
                {rightItem?.callsign || ""}
              </td>
              <td
                className={rightClass}
                data-hex={rightItem?.hex_code ?? ""}
                onClick={gotoHex}
              >
                {rightItem?.origin || ""}
                {rightItem ? " - " : ""}
                {rightItem?.dest || ""}
              </td>
              <td
                className={`text-right ${rightClass}`}
                data-hex={rightItem?.hex_code ?? ""}
                onClick={gotoHex}
              >
                {rightItem ? (
                  <>
                    <span>{`${rightItem.alt} ft`}</span>{" "}
                    <span className={`${rightItem.alt_class} arrow-width`}>
                      {rightItem.alt_arrow}
                    </span>
                  </>
                ) : (
                  ""
                )}
              </td>
              <td
                className={`text-right ${rightClass}`}
                data-hex={rightItem?.hex_code ?? ""}
                onClick={gotoHex}
              >
                {rightItem ? (
                  <>
                    <span>{`${rightItem.gs === "" ? "" : `${rightItem.gs} kts`}`}</span>{" "}
                    <span className={`${rightItem.gs_class} arrow-width`}>
                      {rightItem.gs_arrow}
                    </span>
                  </>
                ) : (
                  ""
                )}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default FlightList;
