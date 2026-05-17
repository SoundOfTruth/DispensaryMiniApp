import { computed, ref } from "vue";
import { defineStore } from "pinia";

import EquipmentApi from "../api/equipments";
import type {
  Equipment,
  CreateEquipment,
  SimpleEquipment,
} from "../types/equipments";
import { useRoute } from "vue-router";
import { useErrorStore } from "./errors";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useEquipmentStore = defineStore("equipmentStore", () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const equipments = ref<Equipment[]>([]);
  const equipment = ref<SimpleEquipment>();

  const count = computed(() => equipments.value.length || 0);

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
    const params = getAllowedParams(route.query);
    try {
      equipments.value = await EquipmentApi.getAll(params);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const loadById = async (id: number) => {
    try {
      equipment.value = await EquipmentApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const create = async (payload: CreateEquipment) => {
    try {
      return await EquipmentApi.create(payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const update = async (id: number, payload: Partial<CreateEquipment>) => {
    try {
      return await EquipmentApi.update(id, payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await EquipmentApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await EquipmentApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  return {
    equipment,
    equipments,
    count,
    loadList,
    loadById,
    create,
    update,
    deleteById,
    deleteList,
  };
});
