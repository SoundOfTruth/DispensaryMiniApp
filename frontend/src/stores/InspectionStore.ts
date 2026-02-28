import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { defineStore } from "pinia";
import { AxiosError } from "axios";

import InspectionApi from "../api/inspections";
import type { Inspection, SimpleInspection } from "../types/inspections";

export const useInspectionStore = defineStore("inspectionStore", () => {
  const route = useRoute();
  const router = useRouter();
  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();
  const err = ref<string>("Загрузка данных...");

  const getAllowedFilters = (filters: Record<string, any>) => {
    const allowedParams = ["page", "department_id", "speciality_id", "search"];
    const cleanParams: Record<string, any> = {};
    Object.keys(filters).forEach((key) => {
      if (allowedParams.includes(key)) {
        cleanParams[key] = filters[key];
      }
    });
    return cleanParams;
  };

  const loadInspections = async () => {
    const filters = getAllowedFilters(route.query);
    try {
      inspections.value = await InspectionApi.getAll(filters);
      if (inspections.value.length == 0 && !filters) {
        err.value = "В базе нет обследований";
      } else {
        err.value = "Ничего не найдено...";
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
      }
    }
  };

  const loadInspection = async (id: number) => {
    try {
      inspection.value = await InspectionApi.get(id);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
        if (error.message == "Request failed with status code 404") {
          router.push("/not-found");
        }
      }
    }
  };

  return {
    inspections,
    inspection,
    err,
    loadInspection,
    loadInspections,
  };
});
