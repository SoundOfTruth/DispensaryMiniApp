import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { defineStore } from "pinia";

import EquipmentTypeApi from "@/api/equipmentTypes";
import { parseApiErrors, type ApiError } from "@/utils/api";

import type {
  SimpleEquipmentType,
  EquipmentType,
  CreateEquipmentType,
} from "@/types/equipmentTypes";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useEquipmentTypeStore = defineStore("equipmentTypeStore", () => {
  const route = useRoute();

  const detailTypes = ref<EquipmentType[]>([]);
  const types = ref<SimpleEquipmentType[]>([]);
  const type = ref<SimpleEquipmentType>();

  const count = computed(() => types.value.length || 0);
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

  const loadDetailList = async () => {
    try {
      detailTypes.value = await EquipmentTypeApi.getAllDetail();
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const loadList = async () => {
    errors.value = [];
    const params = getAllowedParams(route.query);
    try {
      types.value = await EquipmentTypeApi.getAll(params);
      if (types.value.length == 0 && params.search) {
        errors.value = [
          { message: "Ничего не найдено по заданным параметрам." },
        ];
      }
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };
  const loadById = async (id: number) => {
    try {
      type.value = await EquipmentTypeApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };
  const create = async (payload: CreateEquipmentType) => {
    try {
      return await EquipmentTypeApi.create(payload);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };
  const update = async (id: number, payload: CreateEquipmentType) => {
    try {
      return await EquipmentTypeApi.update(id, payload);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await EquipmentTypeApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await EquipmentTypeApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };
  return {
    detailTypes,
    types,
    type,
    errors,
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
