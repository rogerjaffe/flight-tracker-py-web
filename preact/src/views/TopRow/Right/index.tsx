import FlightText from "./FlightText.tsx";
import InfoPanel from "./InfoPanel.tsx";

const Right = () => {
  return (
    <div class="col-span-3 border-black border-l ml-1 mr-1">
      <FlightText />
      <InfoPanel />
    </div>
  );
};

export default Right;
