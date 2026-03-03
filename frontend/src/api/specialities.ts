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

  async getAll() {
    const response = await this.client.get<Speciality[]>("/specialities/");
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<Speciality>(`/specialities/${id}/`);
    return response.data;
  }

  async create(data: CreateSpeciality) {
    const response = await this.client.post<Speciality>(
      "/specialities/",
      JSON.stringify(data),
    );
    return response.data;
  }
}

export default new SpecialitiesApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
