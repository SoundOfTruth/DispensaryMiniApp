import { useAuthStore } from '@/stores/auth';
import { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from 'axios';

export const setAuthToken = async (config: InternalAxiosRequestConfig<any>) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.setAuthorization(authStore.accessToken);
  }
  return config;
};

export const refreshAndSetToken = async (config: InternalAxiosRequestConfig<any>) => {
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

export const refreshTokenOnFall = async (client: AxiosInstance, error: AxiosError) => {
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
        processQueue(new Error('Failed to refresh token'));
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
