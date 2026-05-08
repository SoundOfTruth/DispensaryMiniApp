import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type { CreateEquipment, Equipment } from "@/types/equipments";

class EquipmentApi {
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

  async get(id: number) {
    const response = await this.client.get<Equipment>(`/equipments/${id}/`);
    return response.data;
  }

  async getAll(params: Record<string, any> = {}) {
    const response = await this.client.get<Equipment[]>("/equipments/", {
      params: { ...params },
    });
    return response.data;
  }

  async create(data: CreateEquipment) {
    const response = await this.client.post<Equipment>("/equipments/", data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateEquipment>) {
    const response = await this.client.patch<Equipment>(
      `/equipments/${id}`,
      data,
    );
    return response.data;
  }
  async delete(id: number) {
    await this.client.delete(`/equipments/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/equipments/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new EquipmentApi(baseApiUrl, {
  "content-type": "application/json",
});
