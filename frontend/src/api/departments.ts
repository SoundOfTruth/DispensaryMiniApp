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

  async getAll(): Promise<Department[]> {
    const response = await this.client.get("/departments/");
    return await response.data;
  }

  async get(id: number): Promise<Department> {
    const response = await this.client.get(`/departments/${id}/`);
    return await response.data;
  }

  async create(data: CreateDepartment): Promise<Department> {
    const response = await this.client.post(
      "/departments/",
      JSON.stringify(data),
    );
    return await response.data;
  }
}

export default new DepartmentsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
