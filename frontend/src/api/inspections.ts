import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosError, AxiosInstance } from "axios";
import type {
  Inspection,
  CreateInspection,
  PaginatedInspection,
} from "@/types/inspections";
import { refreshTokenOnFall, setAuthToken } from "@/utils/api";

class InspectionApi {
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
    const response = await this.client.get<PaginatedInspection>(
      "/inspections/",
      {
        params: { ...defaultParams, ...params },
      },
    );
    return response.data;
  }
  async get(id: number) {
    const response = await this.client.get<Inspection>(`/inspections/${id}/`);
    return response.data;
  }

  async create(data: CreateInspection) {
    const response = await this.client.post<Inspection>("/inspections/", data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateInspection>) {
    const response = await this.client.patch<Inspection>(
      `/inspections/${id}`,
      data,
    );
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/inspections/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/inspections/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new InspectionApi(baseApiUrl, {
  "content-type": "application/json",
});
