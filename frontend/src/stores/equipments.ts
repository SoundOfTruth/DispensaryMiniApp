import { computed, ref } from "vue";
import { defineStore } from "pinia";

import EquipmentApi from "../api/equipments";
import type {
  EquipmentsGroupedByType,
  Equipment,
  CreateEquipment,
} from "../types/equipments";
import { parseApiErrors, type ApiError } from "@/utils/api";
import { useRoute, useRouter } from "vue-router";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useEquipmentStore = defineStore("equipmentStore", () => {
  const route = useRoute();
  const router = useRouter();

  const equipmentsGroupedByType = ref<EquipmentsGroupedByType[]>();
  const equipments = ref<Equipment[]>([]);
  const equipment = ref<Equipment>();

  const count = computed(() => equipments.value.length || 0);
  const errors = ref<ApiError[]>([]);

  const getAllowedParams = (filters: Filters): ApiParams => {
    const allowedParams: (keyof Filters)[] = ["search"];
    const params: ApiParams = {};
    Object.entries(filters).forEach(([key, value]) => {
      const param = key as keyof Filters;

      if (
        allowedParams.includes(param) &&
        value !== undefined &&
        value !== null
      ) {
        params[param] = value;
      }
    });
    return params;
  };

  const loadList = async () => {
    errors.value = [];
    const params = getAllowedParams(route.query);
    try {
      equipments.value = await EquipmentApi.getAll(params);
      if (equipments.value.length == 0 && params.search) {
        errors.value = [
          { message: "Ничего не найдено по заданным параметрам." },
        ];
      }
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const loadById = async (id: number) => {
    try {
      equipment.value = await EquipmentApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const create = async (payload: CreateEquipment) => {
    try {
      return await EquipmentApi.create(payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const update = async (id: number, payload: Partial<CreateEquipment>) => {
    try {
      return await EquipmentApi.update(id, payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await EquipmentApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await EquipmentApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  return {
    equipment,
    equipments,
    equipmentsGroupedByType,
    count,
    errors,
    loadList,
    loadById,
    create,
    update,
    deleteById,
    deleteList,
  };
});
