import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { defineStore } from "pinia";

import DepartmentApi from "@/api/departments";

import type { Department, CreateDepartment } from "@/types/departments";
import { useErrorStore } from "./errors";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useDepartmentStore = defineStore("departmentStore", () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const departments = ref<Department[]>([]);
  const department = ref<Department>();

  const count = computed(() => departments.value.length || 0);

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
      departments.value = await DepartmentApi.getAll(params);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const loadById = async (id: number) => {
    try {
      department.value = await DepartmentApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const create = async (payload: CreateDepartment) => {
    try {
      return await DepartmentApi.create(payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  const update = async (id: number, payload: CreateDepartment) => {
    try {
      return await DepartmentApi.update(id, payload);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await DepartmentApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await DepartmentApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };
  return {
    department,
    departments,
    count,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
