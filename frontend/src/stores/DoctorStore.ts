import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { defineStore } from "pinia";
import { AxiosError } from "axios";

import DoctorsApi from "../api/doctors";

import type { Doctor, SimpleDoctor, ApiDoctor } from "../types/doctors";

export const useDoctorStore = defineStore("doctorStore", () => {
  const route = useRoute();
  const router = useRouter();

  const limit = ref<number>(10);
  const doctors = ref<SimpleDoctor[]>();
  const doctor = ref<Doctor>();
  const count = ref<number>(0);
  const err = ref<string>("Загрузка данных...");

  const setLimit = (val: number) => {
    limit.value = val;
  };

  const getAllowedFilters = (filters: Record<string, any>) => {
    const allowedParams = ["page", "department_id", "speciality_id", "search"];
    const cleanParams: Record<string, any> = {};
    Object.keys(filters).forEach((key) => {
      if (allowedParams.includes(key)) {
        if (key == "page") {
          const page = filters.page;
          cleanParams["limit"] = limit.value;
          cleanParams["offset"] = (page - 1) * limit.value;
        } else {
          cleanParams[key] = filters[key];
        }
      }
    });
    cleanParams;
    return cleanParams;
  };

  const loadList = async () => {
    const filters = getAllowedFilters(route.query);
    try {
      const paginatedData = await DoctorsApi.getAll(filters);
      doctors.value = paginatedData.results;
      count.value = paginatedData.count;
      if (doctors.value.length == 0 && !filters) {
        err.value = "В базе нет врачей";
      } else {
        err.value = "Ничего не найдено...";
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code == "ERR_NETWORK") {
          err.value = "Удалённый сервер не отвечает";
        }
      }
    }
  };

  const loadById = async (id: number) => {
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
    count,
    limit,
    err,
    loadById,
    loadList,
    setLimit,
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

export const getComputedDoctor = (doctor: ApiDoctor): Doctor => {
  return {
    ...doctor,
    experience: getYearsWord(doctor.experience_start),
  };
};
