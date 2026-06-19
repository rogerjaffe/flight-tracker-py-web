import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { Fr24FlightDetail } from "../types/Fr24FlightDetail.ts";
import type { FlightListRecord } from "../types/FlightListRecord.ts";
import type { Nullable } from "../types/Nullable.ts";

interface FlightDataState {
  detail: Nullable<Fr24FlightDetail>;
  flightList: { [key: string]: FlightListRecord };
  toDisplay: Nullable<FlightListRecord>;
}

const initialState: FlightDataState = {
  detail: null,
  flightList: {},
  toDisplay: null,
};

const flightSlice = createSlice({
  name: "flight",
  initialState,
  reducers: {
    // Accepts the raw string sent from PySide6
    setFlightData: (_state, action: PayloadAction<string>) => {
      try {
        const parsed = JSON.parse(action.payload);
        console.log(parsed);
        return { ...parsed };
      } catch (e) {
        console.error("Failed to parse Python payload", e);
      }
    },
  },
});

export const { setFlightData } = flightSlice.actions;
export default flightSlice.reducer;
