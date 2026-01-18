import { defineStore } from "pinia";

import { ref } from "vue";

import type { Inspection, SimpleInspection } from "../types/inspections";

import InspectionApi from "../api/inspections";

export const useInspectionStore = defineStore("inspectionStore", () => {
  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();

  const loadInspections = async () => {
    inspections.value = await InspectionApi.getAll();
  };
  const loadInspection = async (id: number) => {
    inspection.value = await InspectionApi.get(id);
  };
  return {
    inspections,
    inspection,
    loadInspection,
    loadInspections
  };
});
