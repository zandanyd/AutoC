// import mock from "../mock/scan_results.json";
import axios from "axios";

export const analyze = (url: string) => {
  // return new Promise((resolve) => {
  //   setTimeout(() => {
  //     resolve({ data: { ...mock, url }, status: 200 });
  //   }, 2000);
  // });
  return axios.post("/api/v1/analyze", { url });
};
