import axios from "axios";
import type { AxiosInstance } from "axios";

import type { Speciality, CreateSpeciality } from "../types/specialities";

class SpecialitiesApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAll(): Promise<Speciality[]> {
    const response = await this.client.get("/specialities/");
    return response.data;
  }

  async get(id: number): Promise<Speciality> {
    const response = await this.client.get(`/specialities/${id}/`);
    return await response.data;
  }

  async create(data: CreateSpeciality): Promise<Speciality> {
    const response = await this.client.post(
      "/specialities/",
      JSON.stringify(data),
    );
    return await response.data;
  }
}

export default new SpecialitiesApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
