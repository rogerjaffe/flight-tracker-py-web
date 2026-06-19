import { configureStore } from "@reduxjs/toolkit";
import appReducer from "./appSlice";
import flightReducer from "./flightSlice";
import {
  type TypedUseSelectorHook,
  useDispatch,
  useSelector,
} from "react-redux";

// Configure the store with your single slice
export const store = configureStore({
  reducer: {
    app: appReducer, // The key 'items' determines the state namespace
    flight: flightReducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
// Create type-safe versions of standard React-Redux hooks
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
