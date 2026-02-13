import { defineStore } from "pinia";

import { ref } from "vue";

import type { Inspection, SimpleInspection } from "../types/inspections";

import InspectionApi from "../api/inspections";
import { AxiosError } from "axios";
import { useRouter } from "vue-router";

export const useInspectionStore = defineStore("inspectionStore", () => {
  const router = useRouter();
  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();
  const err = ref<string>("Загрузка данных...");

  const loadInspections = async () => {
    try {
      inspections.value = await InspectionApi.getAll();
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
