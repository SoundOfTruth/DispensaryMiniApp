import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

import DepartmentApi from '@/api/departments';

import type { Department, CreateDepartment } from '@/types/departments';
import { useErrorStore } from './errors';
import type { ApiSearchParams } from '@/api/base';

export const useDepartmentStore = defineStore('departmentStore', () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const departments = ref<Department[]>([]);
  const department = ref<Department>();

  const count = computed(() => departments.value.length || 0);

  const getRouteParams = (): ApiSearchParams => {
    const routeSearch = route.query.search;
    const search = routeSearch ? String(routeSearch) : undefined;
    return {
      search: search ? search : undefined,
    };
  };
  const loadList = async () => {
    const params = getRouteParams();
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
