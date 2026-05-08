import { computed, ref } from "vue";
import { defineStore } from "pinia";

import SpecialitiesApi from "@/api/specialities";
import type { Speciality, CreateSpeciality } from "@/types/specialities";
import { parseApiErrors, type ApiError } from "@/utils/api";
import { useRoute, useRouter } from "vue-router";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useSpecialityStore = defineStore("specialityStore", () => {
  const route = useRoute();
  const router = useRouter();

  const specialties = ref<Speciality[]>([]);
  const speciality = ref<Speciality>();

  const count = computed(() => specialties.value.length || 0);
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
      specialties.value = await SpecialitiesApi.getAll(params);
      if (specialties.value.length == 0 && params.search) {
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
      speciality.value = await SpecialitiesApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const create = async (payload: CreateSpeciality) => {
    try {
      return await SpecialitiesApi.create(payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const update = async (id: number, payload: CreateSpeciality) => {
    try {
      return await SpecialitiesApi.update(id, payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await SpecialitiesApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await SpecialitiesApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  return {
    speciality,
    specialties,
    count,
    errors,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
