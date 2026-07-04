import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
// import type {Fr24FlightDetail} from "../types/Fr24FlightDetail.ts";
// import type { Nullable } from "../types/Nullable.ts";
import type {
  // FlightInfoRecord,
  FlightInfoTopLeft,
  FlightInfoTopMiddle,
  FlightInfoTopRight,
  RealTimeFlightInfo,
} from "../types/FlightInfoRecord.ts";

interface FlightInfoState {
  top_left: FlightInfoTopLeft;
  top_middle: FlightInfoTopMiddle;
  top_right: FlightInfoTopRight;
  real_time: RealTimeFlightInfo;
}

const initialState: FlightInfoState = {
  top_left: {} as FlightInfoTopLeft,
  top_middle: {} as FlightInfoTopMiddle,
  top_right: {} as FlightInfoTopRight,
  real_time: {} as RealTimeFlightInfo,
};

const flightInfoSlice = createSlice({
  name: "flightInfo",
  initialState,
  reducers: {
    setFlightInfo: (state, action: PayloadAction<any>) => {
      console.log(action.payload);
      return { ...state, ...action.payload };
    },
  },
});

export const { setFlightInfo } = flightInfoSlice.actions;
export default flightInfoSlice.reducer;
