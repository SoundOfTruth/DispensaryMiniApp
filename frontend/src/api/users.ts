import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type { CreateUser, User, PaginatedUsers } from "@/types/users";

class UserApi {
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
  }

  async getAll(params: Record<string, any> = {}) {
    const defaultParams = { limit: 10, offset: 0 };
    const response = await this.client.get<PaginatedUsers>("/users/", {
      params: { ...defaultParams, ...params },
    });
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<User>(`/users/${id}/`);
    return response.data;
  }

  async create(data: CreateUser) {
    const response = await this.client.post<User>("/users/", data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateUser>) {
    const response = await this.client.patch<User>(`/users/${id}/`, data);
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/users/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/users/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new UserApi(baseApiUrl, {
  "content-type": "application/json",
});
