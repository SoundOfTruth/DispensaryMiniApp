import { ref } from "vue";
import { useRoute } from "vue-router";
import { defineStore } from "pinia";

import DoctorApi from "@/api/doctors";
import { parseApiErrors, type ApiError } from "@/utils/api";

interface ApiParams {
  limit: number;
  offset: number;
  department_id?: number;
  speciality_id?: number;
  search?: number;
}

interface Filters {
  page?: number;
  department_id?: number;
  speciality_id?: number;
  search?: string;
}

import type {
  Doctor,
  SimpleDoctor,
  ApiDoctor,
  CreateDoctor,
} from "../types/doctors";

export const useDoctorStore = defineStore("doctorStore", () => {
  const route = useRoute();

  const doctors = ref<SimpleDoctor[]>([]);
  const doctor = ref<Doctor>();
  const apiDoctor = ref<ApiDoctor>();

  const count = ref<number>(0);
  const limit = ref<number>(10);
  const errors = ref<ApiError[]>([]);

  const setLimit = (val: number) => {
    limit.value = val;
  };

  const getAllowedParams = (filters: Filters): ApiParams => {
    const allowedParams: (keyof Filters)[] = [
      "department_id",
      "speciality_id",
      "search",
    ];
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
      const paginatedData = await DoctorApi.getAll(params);
      doctors.value = paginatedData.results;
      count.value = paginatedData.count;
      if (
        paginatedData.count == 0 &&
        (params.search || params.department_id || params.speciality_id)
      ) {
        errors.value = [
          { message: "Ничего не найдено по заданным параметрам" },
        ];
      }
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const loadById = async (id: number) => {
    errors.value = [];
    try {
      const doctorApi = await DoctorApi.get(id);
      apiDoctor.value = doctorApi;
      doctor.value = getComputedDoctor(doctorApi);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await DoctorApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await DoctorApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const create = async (data: CreateDoctor) => {
    try {
      return await DoctorApi.create(data);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const update = async (id: number, data: Partial<CreateDoctor>) => {
    try {
      return await DoctorApi.update(id, data);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  return {
    apiDoctor,
    doctor,
    doctors,
    count,
    limit,
    errors,
    loadById,
    loadList,
    setLimit,
    create,
    update,
    deleteById,
    deleteList,
  };
});

const getYearsWord = (years: number | null): string => {
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
    experience: getYearsWord(doctor.experience_years),
  };
};
