import axios from "axios";
import type { AxiosInstance } from "axios";

import type {
  Inspection,
  CreateInspection,
  PaginatedInspection,
} from "../types/inspections";

class InspectionsApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAll(filters: Record<string, any> = {}) {
    const defaultParams = { limit: 10, offset: 0 };
    const response = await this.client.get<PaginatedInspection>(
      "/inspections/",
      {
        params: { ...defaultParams, ...filters },
      },
    );
    return response.data;
  }
  async get(id: number) {
    const response = await this.client.get<Inspection>(`/inspections/${id}/`);
    return response.data;
  }

  async create(data: CreateInspection) {
    const response = await this.client.post<Inspection>(
      "/inspections/",
      JSON.stringify(data),
    );
    return response.data;
  }
}

export default new InspectionsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
