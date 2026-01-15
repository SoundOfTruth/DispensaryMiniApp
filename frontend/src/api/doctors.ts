import type { Doctor, SimpleDoctor } from "../types/doctors";
import { getComputedDoctor, getComputedDoctors } from "../types/doctors";
class DoctorsApi {
  protected url: string;
  protected headers: Record<string, string>;
  constructor(url: string, headers: Record<string, string>) {
    this.url = url;
    this.headers = headers;
  }
  async getAll(): Promise<SimpleDoctor[]> {
    let response = await fetch(`${this.url}/doctors/`);
    return getComputedDoctors(await response.json())
  }
  async get(id: number): Promise<Doctor> {
    let response = await fetch(`${this.url}/doctors/${id}/`);
    return getComputedDoctor(await response.json());
  }

}

export default new DoctorsApi("http://localhost:8000/api", {
  "content-type": "application/json",
});
