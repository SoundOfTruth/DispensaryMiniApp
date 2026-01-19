import { defineStore } from "pinia";

import { ref } from "vue";

import type { Speciality, CreateSpeciality } from "../types/specialities";

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
  const create = async (payload: CreateSpeciality) => {
    const speciality = await SpecialitiesApi.create(payload);
    console.log(speciality)
  };  
  return {
    speciality,
    specialities,
    loadSpeciality,
    loadSpecialities,
    create,
  };
});
