import type { Inspection, CreateInspection } from "../types/inspections";

class InspectionsApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getAll(): Promise<Inspection[]> {
    let response = await fetch(`${this.url}/inspections/`);
    return (await response.json()) as Inspection[];
  }
  async get(id: number): Promise<Inspection> {
    let response = await fetch(`${this.url}/inspections/${id}/`);
    return (await response.json()) as Inspection;
  }

  async create(data: CreateInspection): Promise<Inspection[]> {
    let payload = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    let response = await fetch(`${this.url}/inspections/`, payload);
    return (await response.json()) as Inspection[];
  }
}

export default new InspectionsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
