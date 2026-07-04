import {
  createSlice,
  type PayloadAction /*, type PayloadAction */,
} from "@reduxjs/toolkit";
import type { Nullable } from "../types/Nullable.ts";
import type { Config } from "../types/Config.ts";

// 2. Define the interface for the slice state
interface ConfigState {
  config: Nullable<Config>;
}

// 3. Provide the initial state using that type
const initialState: ConfigState = {
  config: null,
};

// 4. Create the slice
export const configSlice = createSlice({
  name: "config",
  initialState,
  reducers: {
    setConfig: (state, action: PayloadAction<any>) => {
      try {
        state.config = action.payload;
        console.log(state.config);
      } catch (e) {
        console.error(e);
      }
    },
  },
});

// Export the generated action creators for use in components
export const { setConfig } = configSlice.actions;

// Export the reducer to plug into the store configuration
export default configSlice.reducer;
