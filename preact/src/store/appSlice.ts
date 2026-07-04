import {
  createSlice,
  type PayloadAction /*, type PayloadAction */,
} from "@reduxjs/toolkit";

export type DisplayContent = "flight" | "map" | "distance";

// 2. Define the interface for the slice state
interface AppState {
  displayContent: DisplayContent;
  displayRotate: boolean;
  displayRotateInterval: number;
  darkmode: boolean;
}

const ls = localStorage.getItem("flight-tracker");
let displayRotate = false;
let displayRotateInterval = 30;

if (ls) {
  const lsValues = JSON.parse(ls);
  displayRotate = lsValues.enableSwitching ?? false;
  displayRotateInterval = lsValues.switchDelay ?? 30; // seconds
}

// 3. Provide the initial state using that type
const initialState: AppState = {
  displayContent: "flight",
  displayRotate,
  displayRotateInterval, // Seconds
  darkmode: false,
};

// 4. Create the slice
export const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    // Redux Toolkit uses Immer internally, allowing you to write "mutating" logic safely
    toggleDisplay: (state) => {
      if (state.displayContent === "flight") {
        state.displayContent = "map";
      } else if (state.displayContent === "map") {
        state.displayContent = "distance";
      } else {
        state.displayContent = "flight";
      }
    },
    setToFlightList: (state) => {
      state.displayContent = "flight";
    },
    setRotate: (state, action: PayloadAction<boolean>) => {
      state.displayRotate = action.payload;
    },
    setRotateInterval: (state, action: PayloadAction<number>) => {
      state.displayRotateInterval = action.payload;
    },
    setDarkmode: (state, action: PayloadAction<boolean>) => {
      state.darkmode = action.payload;
    },
  },
});

// Export the generated action creators for use in components
export const {
  toggleDisplay,
  setToFlightList,
  setDarkmode,
  setRotate,
  setRotateInterval,
} = appSlice.actions;

// Export the reducer to plug into the store configuration
export default appSlice.reducer;
