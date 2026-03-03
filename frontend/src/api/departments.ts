import axios from "axios";
import type { AxiosInstance } from "axios";

import type { Department, CreateDepartment } from "../types/departments";

class DepartmentsApi {
  client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAll() {
    const response = await this.client.get<Department[]>("/departments/");
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<Department>(`/departments/${id}/`);
    return response.data;
  }

  async create(data: CreateDepartment) {
    const response = await this.client.post<Department>(
      "/departments/",
      JSON.stringify(data),
    );
    return response.data;
  }
}

export default new DepartmentsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
