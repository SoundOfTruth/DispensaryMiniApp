import { ref } from "vue";
import { defineStore } from "pinia";

import DepartmentsApi from "../api/departments";

import type { Department, CreateDepartment } from "../types/departments";

export const useDepartmentStore = defineStore("departmentStore", () => {
  const departments = ref<Department[]>([]);
  const department = ref<Department>();

  const loadDepartments = async () => {
    departments.value = await DepartmentsApi.getAll();
  };
  const loadDepartment = async (id: number) => {
    department.value = await DepartmentsApi.get(id);
  };
  const create = async (payload: CreateDepartment) => {
    const speciality = await DepartmentsApi.create(payload);
    console.log(speciality);
  };
  return {
    department,
    departments,
    loadDepartment,
    loadDepartments,
    create,
  };
});
