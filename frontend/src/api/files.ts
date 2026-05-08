import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type { FileResponse } from "@/types/files";

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
