import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

import DoctorApi, { type ApiParams } from '@/api/doctors';

interface Filters {
  page?: number;
  department_id?: number;
  speciality_id?: number;
  search?: string;
}

import type { Doctor, SimpleDoctor, ApiDoctor, CreateDoctor } from '../types/doctors';
import { useErrorStore } from './errors';
import { usePaginationStore } from './paginationStore';

export const useDoctorStore = defineStore('doctorStore', () => {
  const route = useRoute();
  const errorStore = useErrorStore();
  const paginationStore = usePaginationStore();

  const doctors = ref<SimpleDoctor[]>([]);
  const doctor = ref<Doctor>();
  const apiDoctor = ref<ApiDoctor>();

  const count = ref<number>(0);

  const getApiParams = (filters: Filters = {}): ApiParams => {
    const allowedParams: (keyof Filters)[] = ['department_id', 'speciality_id', 'search'];
    const paginationParams = filters.page
      ? paginationStore.calcPagination(filters.page)
      : paginationStore.pagination;
    const search = filters.search || route.query.search;
    const params: ApiParams = {
      ...paginationParams,
      search: search ? String(search) : undefined,
    };
    Object.entries(filters).forEach(([key, value]) => {
      const param = key as keyof Filters;

      if (
        param != 'page' &&
        param != 'search' &&
        allowedParams.includes(param) &&
        value !== undefined &&
        value !== null
      ) {
        params[param] = value;
      }
    });
    return params;
  };

  const loadList = async (filters: Filters = {}) => {
    const params = getApiParams(filters);
    try {
      const paginatedData = await DoctorApi.getAll(params);
      doctors.value = paginatedData.results;
      count.value = paginatedData.count;
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const loadById = async (id: number) => {
    try {
      const doctorApi = await DoctorApi.get(id);
      apiDoctor.value = doctorApi;
      doctor.value = getComputedDoctor(doctorApi);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await DoctorApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await DoctorApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const create = async (data: CreateDoctor) => {
    try {
      return await DoctorApi.create(data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const update = async (id: number, data: Partial<CreateDoctor>) => {
    try {
      return await DoctorApi.update(id, data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  return {
    apiDoctor,
    doctor,
    doctors,
    count,
    loadById,
    loadList,
    create,
    update,
    deleteById,
    deleteList,
  };
});

const getYearsWord = (years: number | null): string => {
  if (!years) {
    return '';
  }
  if (years % 10 === 1 && years % 100 !== 11) {
    return `${years}год`;
  } else if (years % 10 >= 2 && years % 10 <= 4 && (years % 100 < 10 || years % 100 >= 20)) {
    return `${years}года`;
  } else {
    return `${years} лет`;
  }
};

export const getComputedDoctor = (doctor: ApiDoctor): Doctor => {
  return {
    ...doctor,
    experience: getYearsWord(doctor.experience_years),
  };
};
