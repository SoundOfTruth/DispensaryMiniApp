import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type { Department, CreateDepartment } from "@/types/departments";

class DepartmentApi {
  client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
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
