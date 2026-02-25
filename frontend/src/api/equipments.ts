import type { EquipmentsGroupedByType } from "../types/equipments";

import axios from "axios";
import type { AxiosInstance } from "axios";

class EquipmentsApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
    });
  }

  async getAllGroupedByType(): Promise<EquipmentsGroupedByType[]> {
    const response = await this.client.get("/equipments/?group_by=type");
    return await response.data;
  }
}

export default new EquipmentsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
