import { configureStore } from "@reduxjs/toolkit";
import configReducer from "./configSlice";
import analysisReducer from "./analysisSlice";

export const store = configureStore({
  reducer: {
    config: configReducer,
    analysis: analysisReducer,
  },
});
