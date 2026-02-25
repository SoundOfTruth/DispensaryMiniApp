import { defineStore } from "pinia";
import { ref } from "vue";

import type { EquipmentsGroupedByType } from "../types/equipments";
import EquipmentApi from "../api/equipments";
import { AxiosError } from "axios";

export const useEquipmentStore = defineStore("equipmentStore", () => {
  const equipmentsGroupedByType = ref<EquipmentsGroupedByType[]>();
  const err = ref<string>("Загрузка данных...");
  const loadEquipmentsGroupedByType = async () => {
    try {
      equipmentsGroupedByType.value = await EquipmentApi.getAllGroupedByType();
      if (equipmentsGroupedByType.value.length == 0) {
        err.value = "В базе нет оборудования";
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
      }
    }
  };
  return { equipmentsGroupedByType, err, loadEquipmentsGroupedByType };
});
