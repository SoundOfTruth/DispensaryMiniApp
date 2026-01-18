import type { InputDoctor, InputDoctorList, CreateDoctor } from "../types/doctors";
class DoctorsApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getAll(): Promise<InputDoctorList[]> {
    const response = await fetch(`${this.url}/doctors/`);
    return await response.json();
  }
  async get(id: number): Promise<InputDoctor> {
    const response = await fetch(`${this.url}/doctors/${id}/`);
    return await response.json();
  }
  async create(data: CreateDoctor): Promise<InputDoctor> {
    const payload = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(`${this.url}/doctors/`, payload);
    return await response.json();
  }
}

export default new DoctorsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
