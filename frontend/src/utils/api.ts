import { AxiosError } from "axios";
import { type Router } from "vue-router";

import { type RouteLocationNormalizedLoadedGeneric as Route } from "vue-router";

export interface ApiError {
  field?: string;
  message: string;
}

export const parseApiErrors = (
  error: unknown,
  route?: Route,
  router?: Router,
): ApiError[] => {
  if (error instanceof AxiosError) {
    if (error.code == "ERR_NETWORK") {
      return [{ message: "Удалённый сервер не отвечает" }];
    }
    if (error.code == "ERR_BAD_RESPONSE") {
      return [{ message: "Внутренняя ошибка сервера" }];
    }
    if (error.code == "ERR_BAD_REQUEST") {
      if (error.response?.status == 404) {
        if (String(route?.name).includes("admin")) {
          router?.push({ name: "admin.notFound" });
        } else {
          router?.push({ name: "notFound" });
        }
        return [];
      }
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
  return [{ message: "Непредвиденная ошибка" }];
};
