import { Fragment } from "preact";
import { useMemo } from "preact/hooks";
import { calculateDistance } from "../../../utilities/calculateDistance";
import useFlightData from "../../../hooks/useFlightData.ts";
import useConfigData from "../../../hooks/useConfigData.ts";

const OriginDestination = ({ isOrigin }: { isOrigin: boolean }) => {
  const { detail, toDisplay } = useFlightData();
  const config = useConfigData();
  const user = config.user;
  const { home_lat, home_lon } = user || {};

  const code = useMemo(() => {
    if (isOrigin) {
      return detail.airport.origin.code.iata ?? "---";
    } else {
      return detail.airport.destination.code.iata ?? "---";
    }
  }, [isOrigin, detail]);

  const city = useMemo(() => {
    if (isOrigin) {
      return detail.airport.origin.position.region.city ?? "";
    } else {
      return detail.airport.destination.position.region.city ?? "";
    }
  }, [isOrigin, detail]);

  const dx = useMemo(() => {
    if (!home_lat || !home_lon) return "";
    if (!toDisplay || toDisplay.position.length === 0) return "";
    const acPosition = toDisplay.position[toDisplay.position.length - 1];
    const apPosition =
      detail.airport[isOrigin ? "origin" : "destination"].position;
    if (!acPosition || !apPosition) return "---";
    return calculateDistance(
      acPosition.latitude,
      acPosition.longitude,
      apPosition.latitude,
      apPosition.longitude,
      "nm",
    );
  }, [home_lat, home_lon, toDisplay]);

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
      <div id={`${isOrigin ? "origin" : "destination"}-dx`}>{dx} nm</div>
    </Fragment>
  );
};

export default OriginDestination;
