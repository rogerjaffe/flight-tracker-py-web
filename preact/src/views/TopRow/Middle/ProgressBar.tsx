import { useMemo } from "preact/hooks";
import { calculateDistance } from "../../utilities/calculateDistance.ts";
import useFlightData from "../../../hooks/useFlightData.ts";

const ProgressBar = () => {
  const { detail, toDisplay } = useFlightData();

  const progress = useMemo(() => {
    if (toDisplay.position.length === 0) return null;
    const { latitude: acLat, longitude: acLon } =
      toDisplay.position[toDisplay.position.length - 1];
    const { latitude: orLat, longitude: orLon } =
      detail.airport.origin.position;
    const { latitude: deLat, longitude: deLon } =
      detail.airport.destination.position;
    const totalDx = calculateDistance(orLat, orLon, deLat, deLon, "nm") ?? 0;
    const fromDx = calculateDistance(orLat, orLon, acLat, acLon, "nm") ?? 0;
    return totalDx === 0 ? 0 : Math.round((fromDx / totalDx) * 100);
  }, [detail, toDisplay]);

  if (progress === null) return null;

  return (
    <div class="progress-container">
      <div class="progress-track">
        <div
          id="progress-bar-value"
          class="progress-bar"
          style={`width: ${progress}%;`}
        ></div>
        <span id="progress-bar-text" class="progress-text">
          {progress}%
        </span>
      </div>
    </div>
  );
};

export default ProgressBar;
