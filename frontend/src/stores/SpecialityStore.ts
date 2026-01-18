import { defineStore } from "pinia";

import { ref } from "vue";

import type { Speciality } from "../types/specialities";

import SpecialitiesApi from "../api/specialities";

export const useSpecialityStore = defineStore("specialityStore", () => {
  const specialities = ref<Speciality[]>([]);
  const speciality = ref<Speciality>();

  const loadSpecialities = async () => {
    specialities.value = await SpecialitiesApi.getAll();
  };
  const loadSpeciality = async (id: number) => {
    speciality.value = await SpecialitiesApi.get(id);
  };
  return {
    speciality,
    specialities,
    loadSpeciality,
    loadSpecialities,
  };
});
