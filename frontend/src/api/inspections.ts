import type { Inspection, CreateInspection } from "../types/inspections";

import axios from "axios";
import type { AxiosInstance } from "axios";

class InspectionsApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAll(): Promise<Inspection[]> {
    const response = await this.client.get("/inspections/");
    return response.data;
  }
  async get(id: number): Promise<Inspection> {
    const response = await this.client.get(`/inspections/${id}/`);
    return response.data as Inspection;
  }

  async create(data: CreateInspection): Promise<Inspection[]> {
    const response = await this.client.post(
      "/inspections/",
      JSON.stringify(data),
    );
    return (await response.data) as Inspection[];
  }
}

export default new InspectionsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
