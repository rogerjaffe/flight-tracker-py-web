import "./app.css";
import TopRow from "./views/TopRow";
import BottomRow from "./views/BottomRow";
import { useSelector } from "react-redux";
import { selectFlightData } from "./hooks/useFlightData.ts";
import { SplashScreen } from "./views/SplashScreen.tsx";

export function App() {
  const { flightList, detail, toDisplay } = useSelector(selectFlightData);
  if (!flightList || !detail || !toDisplay) {
    return <SplashScreen />;
  } else {
    return (
      <div>
        <TopRow />
        <BottomRow />
      </div>
    );
  }
}
