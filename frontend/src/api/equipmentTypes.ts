import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type {
  SimpleEquipmentType,
  EquipmentType,
  CreateEquipmentType,
} from "@/types/equipmentTypes";

class EquipmentTypeApi {
  client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAllDetail() {
    const defaultparams = { detail: true };
    const response = await this.client.get<EquipmentType[]>(
      "/equipment-types/",
      { params: defaultparams },
    );
    return response.data;
  }

  async getAll(params: Record<string, any> = {}) {
    const response = await this.client.get<SimpleEquipmentType[]>(
      "/equipment-types/",
      {
        params: { ...params },
      },
    );
    return response.data;
  }

  async get(id: number) {
    const response = await this.client.get<SimpleEquipmentType>(
      `/equipment-types/${id}/`,
    );
    return response.data;
  }

  async create(data: CreateEquipmentType) {
    const response = await this.client.post<SimpleEquipmentType>(
      "/equipment-types/",
      data,
    );
    return response.data;
  }
  async update(id: number, data: CreateEquipmentType) {
    const response = await this.client.put<SimpleEquipmentType>(
      `/equipment-types/${id}/`,
      data,
    );
    return response.data;
  }

  async delete(id: number) {
    await this.client.delete(`/equipment-types/${id}/`);
  }

  async deleteBulk(ids: number[]) {
    await this.client.delete("/equipment-types/bulk/", {
      params: { ids: ids },
    });
  }
}

export default new EquipmentTypeApi(baseApiUrl, {
  "content-type": "application/json",
});
