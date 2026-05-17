import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { defineStore } from "pinia";

import EquipmentTypeApi from "@/api/equipmentTypes";

import type {
  SimpleEquipmentType,
  EquipmentType,
  CreateEquipmentType,
} from "@/types/equipments";
import { useErrorStore } from "./errors";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useEquipmentTypeStore = defineStore("equipmentTypeStore", () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const detailTypes = ref<EquipmentType[]>([]);
  const types = ref<SimpleEquipmentType[]>([]);
  const type = ref<SimpleEquipmentType>();

  const count = computed(() => types.value.length || 0);

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

  const loadDetailList = async () => {
    try {
      detailTypes.value = await EquipmentTypeApi.getAllDetail();
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const loadList = async () => {
    const params = getAllowedParams(route.query);
    try {
      types.value = await EquipmentTypeApi.getAll(params);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const loadById = async (id: number) => {
    try {
      type.value = await EquipmentTypeApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const create = async (payload: CreateEquipmentType) => {
    try {
      return await EquipmentTypeApi.create(payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const update = async (id: number, payload: CreateEquipmentType) => {
    try {
      return await EquipmentTypeApi.update(id, payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await EquipmentTypeApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await EquipmentTypeApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  return {
    detailTypes,
    types,
    type,
    count,
    loadById,
    loadDetailList,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
