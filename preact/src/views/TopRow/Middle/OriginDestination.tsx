import { Fragment } from "preact";
import { useMemo } from "preact/hooks";
// import { calculateDistance } from "../../../utilities/calculateDistance";
// import useFlightData from "../../../hooks/useFlightData.ts";
import type {
  FlightInfoTopMiddle,
  RealTimeFlightInfo,
} from "../../../types/FlightInfoRecord.ts";
// import useConfigData from "../../../hooks/useConfigData.ts";

const OriginDestination = ({
  topMiddle,
  realTime,
  isOrigin,
}: {
  topMiddle: FlightInfoTopMiddle;
  realTime: RealTimeFlightInfo;
  isOrigin: boolean;
}) => {
  // const { flightInfo } = useFlightData();
  // const { config } = useConfigData();
  // const user = config?.user;
  // const { lat, lon } = user || {};

  const code = useMemo(() => {
    if (isOrigin) {
      return topMiddle?.origin_iata ?? "---";
    } else {
      return topMiddle?.destination_iata ?? "---";
    }
  }, [topMiddle]);

  const city = useMemo(() => {
    if (isOrigin) {
      return topMiddle?.origin_city ?? "";
    } else {
      return topMiddle?.destination_city ?? "";
    }
  }, [isOrigin, topMiddle]);

  // const dx = useMemo(() => {
  //   if (!lat || !lon) return "";
  //   if (!toDisplay || toDisplay.position.length === 0) return "";
  //   const acPosition = toDisplay.position[toDisplay.position.length - 1];
  //   const apPosition =
  //     detail.airport[isOrigin ? "origin" : "destination"].position;
  //   if (!acPosition || !apPosition) return "---";
  //   return calculateDistance(
  //     acPosition.latitude,
  //     acPosition.longitude,
  //     apPosition.latitude,
  //     apPosition.longitude,
  //     "nm",
  //   );
  // }, [lat, lon, toDisplay]);

  return (
    <Fragment>
      <div
        id={`${isOrigin ? "origin" : "destination"}-iata`}
        className="text-8xl font-bold"
      >
        {code}
      </div>
      <div
        id={`${isOrigin ? "origin" : "destination"}-city`}
        className="text-2xl"
      >
        {city}
      </div>
      {isOrigin ? (
        realTime.origin_dx === -1 ? null : (
          <div id="origin-dx">{realTime.origin_dx.toFixed(0)} nm</div>
        )
      ) : realTime.destination_dx === -1 ? null : (
        <div id="destination-dx">{realTime.destination_dx.toFixed(0)} nm</div>
      )}
    </Fragment>
  );
};

export default OriginDestination;
