import { createSlice } from "@reduxjs/toolkit";

const configSlice = createSlice({
  name: "config",
  initialState: {
    appName: "AutoC: Automated IoCs Extraction Tool",
  },
  reducers: {},
});

export default configSlice.reducer;
