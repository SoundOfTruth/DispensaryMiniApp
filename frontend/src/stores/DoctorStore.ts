import { defineStore } from "pinia";

import { ref } from "vue";
import { useRouter } from "vue-router";
import { AxiosError } from "axios";

import DoctorsApi from "../api/doctors";

import type {
  InputDoctor,
  InputDoctorList,
  Doctor,
  SimpleDoctor,
} from "../types/doctors";

export const useDoctorStore = defineStore("doctorStore", () => {
  const router = useRouter();

  const doctors = ref<SimpleDoctor[]>();
  const doctor = ref<Doctor>();
  const err = ref<string>("Загрузка данных...");

  const loadDoctors = async () => {
    try {
      doctors.value = getComputedDoctors(await DoctorsApi.getAll());
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
      }
    }
  };

  const loadDoctor = async (id: number) => {
    try {
      const doctorApi = await DoctorsApi.get(id);
      if (doctorApi) {
        doctor.value = getComputedDoctor(doctorApi);
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
        if (error.message == "Request failed with status code 404") {
          router.push("/not-found");
        }
      }
    }
  };

  return {
    doctor,
    doctors,
    err,
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
