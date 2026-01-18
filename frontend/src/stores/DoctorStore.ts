import { defineStore } from "pinia";

import { ref } from "vue";

import DoctorsApi from "../api/doctors";

import type {
  InputDoctor,
  InputDoctorList,
  Doctor,
  SimpleDoctor,
} from "../types/doctors";

export const useDoctorStore = defineStore("doctorStore", () => {
  const doctors = ref<SimpleDoctor[]>();
  const doctor = ref<Doctor>();
  const loadDoctors = async () => {
    doctors.value = getComputedDoctors(await DoctorsApi.getAll());
  };
  const loadDoctor = async (id: number) => {
    doctor.value = getComputedDoctor(await DoctorsApi.get(id));
  };
  return {
    doctor,
    doctors,
    loadDoctor,
    loadDoctors,
  };
});

const getYearsWord = (years: number | undefined): string => {
  if (!years) {
    return "";
  }
  if (years % 10 === 1 && years % 100 !== 11) {
    return `${years}год`;
  } else if (
    years % 10 >= 2 &&
    years % 10 <= 4 &&
    (years % 100 < 10 || years % 100 >= 20)
  ) {
    return `${years}года`;
  } else {
    return `${years} лет`;
  }
};

export const getComputedDoctor = (doctor: InputDoctor): Doctor => {
  return {
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
    experience: getYearsWord(doctor.experience),
  };
};

export const getComputedDoctors = (data: InputDoctorList[]): SimpleDoctor[] => {
  return data.map((doctor) => ({
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
  }));
};
