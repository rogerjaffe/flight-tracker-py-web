// import { useMemo } from "preact/hooks";
// import { calculateDistance } from "../../utilities/calculateDistance.ts";
// import useFlightData from "../../../hooks/useFlightData.ts";

import type { RealTimeFlightInfo } from "../../../types/FlightInfoRecord.ts";

const ProgressBar = ({ realTime }: { realTime: RealTimeFlightInfo }) => {
  return (
    <div class="progress-container">
      <div class="progress-track">
        <div
          id="progress-bar-value"
          class="progress-bar"
          style={`width: ${realTime.progress.toFixed(0)}%`}
        ></div>
        <span id="progress-bar-text" class="progress-text">
          {realTime.progress.toFixed(0)}%
        </span>
      </div>
    </div>
  );
};

export default ProgressBar;
