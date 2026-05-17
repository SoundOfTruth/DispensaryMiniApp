import { ref } from "vue";
import { defineStore } from "pinia";

import { AxiosError } from "axios";

export interface ApiError {
  field?: string;
  message: string;
}

export const useErrorStore = defineStore("errorStore", () => {
  const errors = ref<ApiError[]>([]);

  const addErrorMessage = (message: string) => {
    errors.value.push({ message: message });
  };
  const setErrorMessage = (message: string) => {
    errors.value = [{ message: message }];
  };
  const clearErrors = () => {
    errors.value = [];
  };

  const parseApiError = (error: unknown) => {
    if (error instanceof AxiosError) {
      if (error.code == "ETIMEDOUT") {
        errors.value = [{ message: "Сервер перегружен." }];
        return;
      }
      if (error.code == "ERR_NETWORK") {
        errors.value = [{ message: "Удалённый сервер не отвечает." }];
        return;
      }
      if (error.code == "ERR_BAD_RESPONSE") {
        errors.value = [{ message: "Внутренняя ошибка сервера." }];
        return;
      }
      if (error.code == "ERR_BAD_REQUEST") {
        const detail = error.response?.data?.detail;
        if (error.status == 400 && typeof detail === "string") {
          errors.value = [{ message: detail }];
          return;
        }
        if (error.status == 422) {
          if (!Array.isArray(detail)) {
            errors.value = [{ message: "Непредвиденная ошибка." }];
            return;
          }
          errors.value = detail.map((err: any) => ({
            field: err.loc?.slice(1).join("."),
            message: err.msg,
          }));
          return;
        }
      }
      errors.value = [{ message: "Непредвиденная ошибка." }];
    }
  };
  return {
    errors,
    addErrorMessage,
    setErrorMessage,
    clearErrors,
    parseApiError,
  };
});
