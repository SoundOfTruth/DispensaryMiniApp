import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosError, AxiosInstance } from "axios";
import type {
  ApiDoctor,
  CreateDoctor,
  PaginatedDoctors,
} from "@/types/doctors";
import { refreshTokenOnFall, setAuthToken } from "@/utils/api";

class DoctorApi {
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

  async getAll(params: Record<string, any> = {}) {
    const defaultParams = { limit: 10, offset: 0 };
    const response = await this.client.get<PaginatedDoctors>("/doctors/", {
      params: { ...defaultParams, ...params },
    });
    return response.data;
  }
  async get(id: number) {
    const response = await this.client.get<ApiDoctor>(`/doctors/${id}/`);
    return response.data;
  }
  async create(data: CreateDoctor) {
    const response = await this.client.post<ApiDoctor>("/doctors/", data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateDoctor>) {
    const response = await this.client.patch<ApiDoctor>(
      `/doctors/${id}/`,
      data,
    );
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/doctors/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/doctors/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new DoctorApi(baseApiUrl, {
  "content-type": "application/json",
});
