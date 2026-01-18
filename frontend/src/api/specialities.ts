import type { Speciality, CreateSpeciality } from "../types/specialities";
class SpecialitiesApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getAll(): Promise<Speciality[]> {
    const response = await fetch(`${this.url}/specialities/`);
    return await response.json();
  }
  async get(id: number): Promise<Speciality> {
    const response = await fetch(`${this.url}/specialities/${id}/`);
    return await response.json();
  }
  async create(data: CreateSpeciality): Promise<Speciality> {
    const payload = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(`${this.url}/specialities/`, payload);
    return await response.json();
  }
}

export default new SpecialitiesApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
