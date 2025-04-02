import { createSlice } from "@reduxjs/toolkit";

const analysisSlice = createSlice({
  name: "analysis",
  initialState: {
    url: null,
    keywords: [],
    qna: [],
    iocs: [],
  },
  reducers: {
    setAnalysisResults: (state, action) => {
      state.url = action.payload.url;
      state.keywords = action.payload.keywords;
      state.qna = action.payload.qna;
      state.iocs = action.payload.iocs;
    },
    clearAnalysisResults: (state) => {
      state.url = null;
      state.keywords = [];
      state.qna = [];
      state.iocs = [];
    },
  },
});
export const { setAnalysisResults, clearAnalysisResults } =
  analysisSlice.actions;
export default analysisSlice.reducer;
