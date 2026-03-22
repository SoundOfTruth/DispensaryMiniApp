import { ref } from "vue";
import { defineStore } from "pinia";

import SpecialitiesApi from "../api/specialities";
import type { Speciality, CreateSpeciality } from "../types/specialities";

export const useSpecialityStore = defineStore("specialityStore", () => {
  const specialities = ref<Speciality[]>([]);
  const speciality = ref<Speciality>();

  const loadList = async () => {
    specialities.value = await SpecialitiesApi.getAll();
  };
  const loadById = async (id: number) => {
    speciality.value = await SpecialitiesApi.get(id);
  };
  const create = async (payload: CreateSpeciality) => {
    const speciality = await SpecialitiesApi.create(payload);
    console.log(speciality);
  };
  return {
    speciality,
    specialities,
    loadById,
    loadList,
    create,
  };
});
