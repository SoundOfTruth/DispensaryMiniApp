import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosError, AxiosInstance } from "axios";
import type { FileResponse } from "@/types/files";
import { refreshTokenOnFall, setAuthToken } from "@/utils/api";

class FilesApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
      paramsSerializer: {
        indexes: null,
      },
    });
    this.client.interceptors.request.use(
      (config) => setAuthToken(config),
      (error) => Promise.reject(error),
    );
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => await refreshTokenOnFall(this.client, error),
    );
  }

  async create(file: any) {
    const data = new FormData();
    data.append("file", file);
    const response = await this.client.post<FileResponse>("/upload/", data);
    return response.data;
  }
}

export default new FilesApi(baseApiUrl, {
  "content-type": "multipart/form-data",
});
