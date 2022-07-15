import axios from "axios";
import config from "../../config.client.json";

export const http = axios.create({
  baseURL: `http://${config.apiDomain}:${config.apiPort}${config.apiBase}`,
  withCredentials: true,
});
