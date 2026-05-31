import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

import InspectionApi from '../api/inspections';
import type { CreateInspection, Inspection, SimpleInspection } from '../types/inspections';
import { useErrorStore } from './errors';
import type { ApiParams } from '@/api/inspections';
import { usePaginationStore } from './paginationStore';

interface Filters {
  page?: number;
  search?: string;
  filled?: boolean;
}

export const useInspectionStore = defineStore('inspectionStore', () => {
  const route = useRoute();
  const errorStore = useErrorStore();
  const paginationStore = usePaginationStore();

  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();

  const count = ref<number>(0);

  const getApiParams = (filters: Filters = {}): ApiParams => {
    const search = filters.search || route.query.search;
    const paginationParams = filters.page
      ? paginationStore.calcPagination(filters.page)
      : paginationStore.pagination;
    return {
      ...paginationParams,
      search: search ? String(search) : undefined,
    };
  };

  const loadList = async (filters: Filters = {}) => {
    try {
      const paginatedData = await InspectionApi.getAll(getApiParams(filters));
      inspections.value = paginatedData.results;
      count.value = paginatedData.count;
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const loadPublicList = async () => {
    const params = getApiParams();
    try {
      const paginatedData = await InspectionApi.getAll({ ...params, filled: true });
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
    loadById,
    loadList,
    loadPublicList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
