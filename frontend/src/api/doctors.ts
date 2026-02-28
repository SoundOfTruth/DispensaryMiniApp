import axios from "axios";
import type { AxiosInstance } from "axios";

import type {
  InputDoctor,
  InputDoctorList,
  CreateDoctor,
} from "../types/doctors";

class DoctorsApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAll(filters: Record<string, any> = {}) {
    const response = await this.client.get<InputDoctorList[]>("/doctors/", {
      params: filters,
    });
    return response.data;
  }
  async get(id: number) {
    const response = await this.client.get<InputDoctor | undefined>(
      `/doctors/${id}/`,
    );
    return response.data;
  }
  async create(data: CreateDoctor) {
    const response = await this.client.post<InputDoctor>(
      "/doctors/",
      JSON.stringify(data),
    );
    return response.data;
  }
}

export default new DoctorsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
