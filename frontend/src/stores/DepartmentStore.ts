import { defineStore } from "pinia";

import { ref } from "vue";

import type { Department } from "../types/departments";

import DepartmentsApi from "../api/departments";

export const useDepartmentStore = defineStore("departmentStore", () => {
  const departments = ref<Department[]>([]);
  const department = ref<Department>();

  const loadDepartments = async () => {
    departments.value = await DepartmentsApi.getAll();
  };
  const loadDepartment = async (id: number) => {
    department.value = await DepartmentsApi.get(id);
  };
  return {
    department,
    departments,
    loadDepartment,
    loadDepartments,
  };
});
