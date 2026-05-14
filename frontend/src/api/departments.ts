import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosError, AxiosInstance } from "axios";
import type { Department, CreateDepartment } from "@/types/departments";
import { refreshTokenOnFall, setAuthToken } from "@/utils/api";

class DepartmentApi {
  client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
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
    const response = await this.client.get<Department[]>("/departments/", {
      params: { ...params },
    });
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<Department>(`/departments/${id}/`);
    return response.data;
  }

  async create(data: CreateDepartment) {
    const response = await this.client.post<Department>("/departments/", data);
    return response.data;
  }
  async update(id: number, data: CreateDepartment) {
    const response = await this.client.put<Department>(
      `/departments/${id}/`,
      data,
    );
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/departments/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/departments/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new DepartmentApi(baseApiUrl, {
  "content-type": "application/json",
});
