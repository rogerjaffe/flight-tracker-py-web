import "./app.css";
import TopRow from "./views/TopRow";
import BottomRow from "./views/BottomRow";
import { SplashScreen } from "./views/SplashScreen.tsx";
import useConfigData from "./hooks/useConfigData.ts";
import { useAppSelector } from "./store";

export function App() {
  const configData = useConfigData();
  const flightInfo = useAppSelector((state) => state.flightInfo);

  if (!configData || !flightInfo.top_left.callsign) {
    return <SplashScreen />;
  } else {
    return (
      <div className="grid grid-cols-8 grid-rows-5 gap-0">
        <TopRow />
        <BottomRow />
      </div>
    );
  }
}
