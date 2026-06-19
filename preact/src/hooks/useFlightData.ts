import { type RootState, useAppSelector } from "../store";

// A normal selector that can return your data or null
export const selectFlightData = (state: RootState) => state.flight;

export function useFlightData() {
  const { flightList, detail, toDisplay } = useAppSelector(selectFlightData);

  // This runtime check guarantees to TypeScript that 'data' cannot be null past this line
  if (!flightList || !detail || !toDisplay) {
    throw new Error(
      "useLoadedUser was called before the data was initialized. " +
        "Ensure this component is only rendered inside a loaded MainPage state.",
    );
  }

  // TypeScript automatically infers this return type as non-null
  return { flightList, detail, toDisplay };
}

export default useFlightData;
