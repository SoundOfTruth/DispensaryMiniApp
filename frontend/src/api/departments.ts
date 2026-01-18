import type { Department, CreateDepartment } from "../types/departments";
class DepartmentsApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getAll(): Promise<Department[]> {
    const response = await fetch(`${this.url}/departments/`);
    return await response.json();
  }
  async get(id: number): Promise<Department> {
    const response = await fetch(`${this.url}/departments/${id}/`);
    return await response.json();
  }
  async create(data: CreateDepartment): Promise<Department> {
    const payload = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(`${this.url}/departments/`, payload);
    return await response.json();
  }
}

export default new DepartmentsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
