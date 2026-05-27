import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

import InspectionApi from '../api/inspections';
import type { CreateInspection, Inspection, SimpleInspection } from '../types/inspections';
import { useErrorStore } from './errors';
import type { Filters } from './base';
import type { ApiParams } from '@/api/base';

export const useInspectionStore = defineStore('inspectionStore', () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();

  const count = ref<number>(0);
  const limit = ref<number>(10);

  const getApiParams = (params: Filters): ApiParams => {
    const allowedParams: (keyof Filters)[] = ['search'];
    const page = params?.page || 1;
    const apiParams: ApiParams = {
      offset: (page - 1) * limit.value,
      limit: limit.value,
    };
    Object.entries(params).forEach(([key, value]) => {
      const param = key as keyof Filters;
      if (
        param != 'page' &&
        allowedParams.includes(param) &&
        value !== undefined &&
        value !== null
      ) {
        apiParams[param] = value;
      }
    });
    return apiParams;
  };

  const loadList = async (filters: Filters = {}) => {
    const routeParams = getApiParams(route.query);
    const params = getApiParams(filters);
    try {
      const paginatedData = await InspectionApi.getAll(
        Object.keys(filters).length !== 0 ? params : routeParams
      );
      inspections.value = paginatedData.results;
      count.value = paginatedData.count;
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const loadById = async (id: number) => {
    try {
      inspection.value = await InspectionApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const create = async (data: CreateInspection) => {
    try {
      return await InspectionApi.create(data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const update = async (id: number, data: Partial<CreateInspection>) => {
    try {
      return await InspectionApi.update(id, data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await InspectionApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await InspectionApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  return {
    inspection,
    inspections,
    count,
    limit,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
