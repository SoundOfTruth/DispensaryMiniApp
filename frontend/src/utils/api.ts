import { useAuthStore } from "@/stores/auth";
import {
  AxiosError,
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from "axios";

export interface ApiError {
  field?: string;
  message: string;
}

export const parseApiErrors = (error: unknown): ApiError[] => {
  if (error instanceof AxiosError) {
    if (error.code == "ETIMEDOUT") {
      return [{ message: "Сервер перегружен." }];
    }
    if (error.code == "ERR_NETWORK") {
      return [{ message: "Удалённый сервер не отвечает." }];
    }
    if (error.code == "ERR_BAD_RESPONSE") {
      return [{ message: "Внутренняя ошибка сервера." }];
    }
    if (error.code == "ERR_BAD_REQUEST") {
      const detail = error.response?.data?.detail;
      if (error.status == 400) {
        return [{ message: detail }];
      }
      if (error.status == 422) {
        const detail = error.response?.data?.detail;
        if (!Array.isArray(detail)) return [];
        return detail.map((err: any) => ({
          field: err.loc?.slice(1).join("."),
          message: err.msg,
        }));
      }
    }
  }
  return [{ message: "Непредвиденная ошибка." }];
};

export const setAuthToken = async (config: InternalAxiosRequestConfig<any>) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.setAuthorization(authStore.accessToken);
  }
  return config;
};

export const refreshAndSetToken = async (
  config: InternalAxiosRequestConfig<any>,
) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.setAuthorization(authStore.accessToken);
  } else if (authStore.isAuthenticated) {
    try {
      await authStore.refreshAccessToken();
      config.headers.setAuthorization(authStore.accessToken);
    } catch (error) {
      console.error(error);
    }
  }
  return config;
};

let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

const processQueue = (error: unknown) => {
  const authStore = useAuthStore();
  failedQueue.forEach((promise) => {
    if (error !== null) {
      promise.reject(error);
    } else if (authStore.accessToken) {
      promise.resolve(authStore.accessToken);
    }
  });

  failedQueue = [];
};

export const refreshTokenOnFall = async (
  client: AxiosInstance,
  error: AxiosError,
) => {
  const origRequest = error.config as InternalAxiosRequestConfig & {
    _retry?: boolean;
  };
  if (origRequest._retry) {
    return Promise.reject(error);
  }

  const authStore = useAuthStore();
  if (error.status === 401 && authStore.accessToken !== null) {
    try {
      await authStore.refreshAccessToken();
      if (authStore.accessToken) {
        processQueue(null);
      } else {
        processQueue(new Error("Failed to refresh token"));
      }
      return client(origRequest);
    } catch (err) {
      return new Promise((resolve, reject) => {
        failedQueue.push({
          resolve: (token: string) => {
            origRequest.headers.setAuthorization(token);
            resolve(client(origRequest));
          },

          reject,
        });
      });
    }
  }
  return Promise.reject(error);
};
