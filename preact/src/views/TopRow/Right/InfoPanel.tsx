import NumberWithArrow from "../../utilities/NumberWithArrow.tsx";
import useFlightData from "../../../hooks/useFlightData.ts";

const InfoPanel = () => {
  const { toDisplay } = useFlightData();
  const { position, hex } = toDisplay;
  const squawk = position
    ? position[position.length - 1].squawk
      ? position[position.length - 1].squawk
      : "None"
    : "None";
  return (
    <table
      id="info-panel-1"
      class="table-auto border-collapse text-left w-full"
    >
      <tbody class="divide-y">
        <tr>
          <td>Altitude:</td>
          <td>
            <NumberWithArrow
              position={position}
              prop="altitude"
              units="ft"
              direction="ud"
            />
          </td>
        </tr>
        <tr>
          <td>Groundspeed:</td>
          <td>
            <NumberWithArrow
              position={position}
              prop="ground_speed"
              units="kts"
              direction="ud"
            />
          </td>
        </tr>
        <tr>
          <td>Heading:</td>
          <td>
            <NumberWithArrow
              position={position}
              prop="heading"
              units="°"
              direction="lr"
            />
          </td>
        </tr>
        <tr>
          <td>Squawk:</td>
          <td id="squawk">{squawk}</td>
        </tr>
        <tr>
          <td>ICAO:</td>
          <td>{hex ? hex : ""}</td>
        </tr>
      </tbody>
    </table>
  );
};

export default InfoPanel;
