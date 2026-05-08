import type { RouteRecordRaw } from "vue-router";

export const specialityRoutes: RouteRecordRaw[] = [
  {
    path: "specialties",
    name: "admin.specialties",
    component: () => import("@/views/admin/AdminSpecialtiesView.vue"),
  },
  {
    path: "specialties/create",
    name: "admin.specialties.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/SpecialityForm.vue"),
  },
  {
    path: "specialties/:id(\\d+)/edit",
    name: "admin.specialties.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/SpecialityForm.vue"),
  },
  {
    path: "specialties/:id(\\d+)",
    name: "admin.specialties.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/SpecialityForm.vue"),
  },
];
