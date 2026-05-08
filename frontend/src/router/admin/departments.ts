import type { RouteRecordRaw } from "vue-router";

export const departmentRoutes: RouteRecordRaw[] = [
  {
    path: "departments",
    name: "admin.departments",
    component: () => import("@/views/admin/AdminDepartmentsVeiw.vue"),
  },
  {
    path: "departments/create",
    name: "admin.departments.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/DepartmentForm.vue"),
  },
  {
    path: "departments/:id(\\d+)/edit",
    name: "admin.departments.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/DepartmentForm.vue"),
  },
  {
    path: "departments/:id(\\d+)",
    name: "admin.departments.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/SpecialityForm.vue"),
  },
];
