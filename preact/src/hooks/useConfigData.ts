import { type RootState, useAppSelector } from "../store";

// A normal selector that can return your data or null
export const selectConfigState = (state: RootState) => state.app.config;

export function useConfigData() {
  const data = useAppSelector(selectConfigState);

  // This runtime check guarantees to TypeScript that 'data' cannot be null past this line
  if (data === null || data === undefined) {
    throw new Error(
      "useLoadedUser was called before the data was initialized. " +
        "Ensure this component is only rendered inside a loaded MainPage state.",
    );
  }

  // TypeScript automatically infers this return type as non-null
  return data;
}

export default useConfigData;
