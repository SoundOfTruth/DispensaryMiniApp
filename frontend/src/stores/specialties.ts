import { computed, ref } from 'vue';
import { defineStore } from 'pinia';

import SpecialitiesApi from '@/api/specialities';
import type { Speciality, CreateSpeciality } from '@/types/specialities';
import { useRoute } from 'vue-router';
import { useErrorStore } from './errors';
import type { ApiSearchParams } from '@/api/base';

export const useSpecialityStore = defineStore('specialityStore', () => {
  const route = useRoute();
  const errorStore = useErrorStore();

  const specialties = ref<Speciality[]>([]);
  const speciality = ref<Speciality>();

  const count = computed(() => specialties.value.length || 0);

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
