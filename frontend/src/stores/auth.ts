import { ref } from "vue";
import { defineStore } from "pinia";

import AuthApi from "@/api/auth";
import { AxiosError } from "axios";
import type { LoginSchema } from "@/types/auth";
import { useErrorStore } from "./errors";

export const useAuthStore = defineStore("authStore", () => {
  const errorStore = useErrorStore();

  const accessToken = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(
    localStorage.getItem("isAuthenticated") === "true" ? true : false,
  );
  const isRefreshing = ref<boolean>(false);

  const setAccessToken = (token: string | null, tokenType?: string) => {
    if (tokenType && token) {
      accessToken.value = `${tokenType} ${token}`;
      localStorage.setItem("isAuthenticated", "true");
      isAuthenticated.value = true;
    } else {
      accessToken.value = null;
      localStorage.removeItem("isAuthenticated");
      isAuthenticated.value = false;
    }
  };

  const login = async (data: LoginSchema) => {
    try {
      const tokenResponse = await AuthApi.login(data.email, data.password);
      setAccessToken(tokenResponse.access_token, tokenResponse.token_type);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const refreshAccessToken = async () => {
    if (isRefreshing.value) {
      throw new Error("isRefreshing");
    }
    if (!isAuthenticated.value) {
      throw new Error("not authenticated");
    }
    isRefreshing.value = true;
    try {
      const response = await AuthApi.refresh();
      setAccessToken(response.access_token, response.token_type);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.status === 401) {
          setAccessToken(null);
        } else {
          accessToken.value = null;
        }
        errorStore.parseApiError(error);
      }
    } finally {
      isRefreshing.value = false;
    }
  };

  const logout = async () => {
    try {
      await AuthApi.logout();
      setAccessToken(null);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  return { accessToken, isAuthenticated, login, refreshAccessToken, logout };
});
