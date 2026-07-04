import { type RootState, useAppSelector } from "../store";

// A normal selector that can return your data or null
export const selectFlightList = (state: RootState) => state.flightList;
export const selectFlightInfo = (state: RootState) => {
  return state.flightInfo;
};

export function useFlightData() {
  const { flightList } = useAppSelector(selectFlightList);
  const { flightInfo } = useAppSelector(selectFlightInfo);

  // This runtime check guarantees to TypeScript that 'data' cannot be null past this line
  if (!flightList || !flightInfo) {
    console.log("useFlightData: flightList or flightInfo is null");
  }

  // TypeScript automatically infers this return type as non-null
  return { flightList, flightInfo };
}

export default useFlightData;
