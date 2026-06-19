import {
  createSlice,
  type PayloadAction /*, type PayloadAction */,
} from "@reduxjs/toolkit";

export type DisplayContent = "flight" | "map" | "distance";

// 2. Define the interface for the slice state
interface AppState {
  displayContent: DisplayContent;
  displayRotate: boolean;
  config: Record<string, any> | null;
}

// 3. Provide the initial state using that type
const initialState: AppState = {
  displayContent: "flight",
  displayRotate: false,
  config: null,
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
    toggleRotate: (state) => {
      state.displayRotate = !state.displayRotate;
    },
    setAppConfig: (state, action: PayloadAction<string>) => {
      try {
        state.config = JSON.parse(action.payload);
        console.log(state.config);
      } catch (e) {
        console.error(e);
      }
    },
  },
});

// Export the generated action creators for use in components
export const {toggleDisplay, toggleRotate, setAppConfig} = appSlice.actions;

// Export the reducer to plug into the store configuration
export default appSlice.reducer;
