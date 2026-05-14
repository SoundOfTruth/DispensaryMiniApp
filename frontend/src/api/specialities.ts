import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosError, AxiosInstance } from "axios";
import type { Speciality, CreateSpeciality } from "@/types/specialities";
import { refreshTokenOnFall, setAuthToken } from "@/utils/api";

class SpecialtiesApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
      paramsSerializer: {
        indexes: null,
      },
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
    const response = await this.client.get<Speciality[]>("/specialties/", {
      params: { ...params },
    });
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<Speciality>(`/specialties/${id}/`);
    return response.data;
  }

  async create(data: CreateSpeciality) {
    const response = await this.client.post<Speciality>("/specialties/", data);
    return response.data;
  }

  async update(id: number, data: CreateSpeciality) {
    const response = await this.client.put<Speciality>(
      `/specialities/${id}/`,
      data,
    );
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/specialties/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/specialties/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new SpecialtiesApi(baseApiUrl, {
  "content-type": "application/json",
});
