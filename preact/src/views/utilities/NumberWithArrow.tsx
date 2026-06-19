import type { Position } from "../../types/BackendFlightPayload.ts";
import type { Nullable } from "../../types/Nullable.ts";
import getAltitudeColor from "./getAltitudeColor.ts";

export type Direction = "ud" | "lr";

const arrows = {
  up: "▲",
  right: "▶",
  down: "▼",
  left: "◀",
};

const NumberWithArrow = ({
  position,
  prop,
  units,
  direction,
}: {
  position: Nullable<Position[]>;
  prop: keyof Position;
  units?: string;
  direction: Direction;
}) => {
  if (!position || position.length == 0) {
    return (
      <div class="number-arrow-container">
        <span>--- {units} </span>
        <span>&nbsp;</span>
      </div>
    );
  }
  let x0 =
    position.length >= 2
      ? position[position.length - 2][prop]
      : position[position.length - 1][prop];
  let x1 = position[position.length - 1][prop];
  let arrow = null;
  let className = "";
  if (direction === "ud") {
    if (x0 < x1) {
      className = "text-green-500 arrow-font ud-arrow";
      arrow = <span className={className}>{arrows.up}</span>;
    } else if (x0 > x1) {
      className = "text-red-500 arrow-font ud-arrow";
      arrow = <span className={className}>{arrows.down}</span>;
    } else {
      className = "text-gray-500 arrow-font ud-arrow";
      arrow = (
        <span className={className}>
          <hr />
        </span>
      );
    }
  } else if (direction === "lr") {
    if (x0 < x1) {
      className = "arrow-font text-red-500 lr-arrow";
      arrow = <span className={className}>{arrows.left}</span>;
    } else if (x0 > x1) {
      className = "arrow-font text-green-500 lr-arrow";
      arrow = <span className={className}>{arrows.right}</span>;
    } else {
      className = "arrow-font text-gray-500 lr-arrpw";
      arrow = <span className={className}>&#10074;</span>;
    }
  }
  const alt = typeof x1 === "number" ? x1 : 0;
  const rgb = prop === "altitude" ? getAltitudeColor(alt) : null;
  return (
    <div class="number-arrow-container">
      <span style={rgb ? { color: rgb } : ""}>
        {x1.toLocaleString()} {units}{" "}
      </span>
      {arrow}
    </div>
  );
};

export default NumberWithArrow;
