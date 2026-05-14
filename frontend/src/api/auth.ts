import axios from "axios";

import { baseApiUrl } from "./base";

import type { AxiosInstance } from "axios";
import type { JWTResponse } from "@/types/auth";

class AuthApi {
  protected client: AxiosInstance;

  constructor(url: string, headers: Record<string, string>) {
    this.client = axios.create({
      baseURL: url,
      headers: headers,
      timeout: 7000,
      withCredentials: true,
    });
  }

  async login(email: string, password: string) {
    const response = await this.client.post<JWTResponse>("/auth/login/", {
      email: email,
      password: password,
    });
    return response.data;
  }

  async refresh() {
    const response = await this.client.post<JWTResponse>("/auth/refresh/");
    return response.data;
  }

  async logout() {
    await this.client.post<JWTResponse>("/auth/logout/");
  }
}

export default new AuthApi(baseApiUrl, {
  "content-type": "application/json",
});
