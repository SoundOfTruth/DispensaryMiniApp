import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { defineStore } from "pinia";

import InspectionApi from "../api/inspections";
import type {
  CreateInspection,
  Inspection,
  SimpleInspection,
} from "../types/inspections";
import { parseApiErrors, type ApiError } from "@/utils/api";

interface ApiParams {
  limit: number;
  offset: number;
  search?: number;
}

interface Filters {
  page?: number;
  search?: string;
}

export const useInspectionStore = defineStore("inspectionStore", () => {
  const route = useRoute();
  const router = useRouter();

  const inspections = ref<SimpleInspection[]>([]);
  const inspection = ref<Inspection>();

  const count = ref<number>(0);
  const limit = ref<number>(10);
  const errors = ref<ApiError[]>([]);

  const getAllowedParams = (filters: Filters): ApiParams => {
    const allowedParams: (keyof Filters)[] = ["search"];
    const page = filters?.page || 1;
    const params: ApiParams = {
      offset: (page - 1) * limit.value,
      limit: limit.value,
    };
    Object.entries(filters).forEach(([key, value]) => {
      const param = key as keyof Filters;
      if (
        param != "page" &&
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
      const paginatedData = await InspectionApi.getAll(params);
      inspections.value = paginatedData.results;
      count.value = paginatedData.count;
      if (paginatedData.count == 0 && params.search) {
        errors.value = [
          { message: "Ничего не найдено по заданным параметрам" },
        ];
      }
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const loadById = async (id: number) => {
    errors.value = [];
    try {
      inspection.value = await InspectionApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const create = async (data: CreateInspection) => {
    try {
      return await InspectionApi.create(data);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const update = async (id: number, data: Partial<CreateInspection>) => {
    try {
      return await InspectionApi.update(id, data);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await InspectionApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await InspectionApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error, route, router);
    }
  };

  return {
    inspection,
    inspections,
    count,
    limit,
    errors,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});
