import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { defineStore } from "pinia";

import DepartmentApi from "@/api/departments";
import { parseApiErrors, type ApiError } from "@/utils/api";

import type { Department, CreateDepartment } from "@/types/departments";

interface ApiParams {
  search?: number;
}

interface Filters {
  search?: string;
}

export const useDepartmentStore = defineStore("departmentStore", () => {
  const route = useRoute();
  const router = useRouter();

  const departments = ref<Department[]>([]);
  const department = ref<Department>();

  const count = computed(() => departments.value.length || 0);
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
      departments.value = await DepartmentApi.getAll(params);
      if (departments.value.length == 0 && params.search) {
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
      department.value = await DepartmentApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const create = async (payload: CreateDepartment) => {
    try {
      return await DepartmentApi.create(payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  const update = async (id: number, payload: CreateDepartment) => {
    try {
      return await DepartmentApi.update(id, payload);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await DepartmentApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await DepartmentApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };
  return {
    department,
    departments,
    errors,
    count,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
