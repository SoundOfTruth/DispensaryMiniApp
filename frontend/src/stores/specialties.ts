import { computed, ref } from "vue";
import { defineStore } from "pinia";

import SpecialitiesApi from "@/api/specialities";
import type { Speciality, CreateSpeciality } from "@/types/specialities";
import { useRoute } from "vue-router";
import { useErrorStore } from "./errors";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useSpecialityStore = defineStore("specialityStore", () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const specialties = ref<Speciality[]>([]);
  const speciality = ref<Speciality>();

  const count = computed(() => specialties.value.length || 0);

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
      specialties.value = await SpecialitiesApi.getAll(params);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const loadById = async (id: number) => {
    try {
      speciality.value = await SpecialitiesApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const create = async (payload: CreateSpeciality) => {
    try {
      return await SpecialitiesApi.create(payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const update = async (id: number, payload: CreateSpeciality) => {
    try {
      return await SpecialitiesApi.update(id, payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await SpecialitiesApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await SpecialitiesApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  return {
    speciality,
    specialties,
    count,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
