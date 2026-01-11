import type { Inspection } from "../types/inspections";

class InspectionsApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getInspections(): Promise<Inspection[]> {
    let response = await fetch(`${this.url}/inspections/`);
    return (await response.json()) as Inspection[];
  }
  async getInspection(id: number): Promise<Inspection> {
    let response = await fetch(`${this.url}/inspections/${id}/`);
    return (await response.json()) as Inspection;
  }
}

export default new InspectionsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
