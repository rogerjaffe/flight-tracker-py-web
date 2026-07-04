import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
// import type { Fr24FlightDetail } from "../types/Fr24FlightDetail.ts";
import type { FlightListRecord } from "../types/FlightListRecord.ts";

// import type { Nullable } from "../types/Nullable.ts";

interface FlightListState {
  flightList: FlightListRecord[];
}

const initialState: FlightListState = {
  flightList: [],
};

const flightListSlice = createSlice({
  name: "flightList",
  initialState,
  reducers: {
    // Accepts the raw string sent from PySide6
    setFlightList: (state, action: PayloadAction<any>) => {
      console.log(action.payload);
      state.flightList = { ...action.payload };
    },
  },
});

export const { setFlightList } = flightListSlice.actions;
export default flightListSlice.reducer;
