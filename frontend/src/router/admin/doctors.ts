import type { RouteRecordRaw } from "vue-router";

export const doctorsRoute: RouteRecordRaw[] = [
  {
    path: "doctors",
    name: "admin.doctors",
    component: () => import("@/views/admin/AdminDoctorsView.vue"),
  },
  {
    path: "doctors/create",
    name: "admin.doctors.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/DoctorForm.vue"),
  },
  {
    path: "doctors/:id(\\d+)/edit",
    name: "admin.doctors.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/DoctorForm.vue"),
  },
  {
    path: "doctors/:id(\\d+)",
    name: "admin.doctors.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/DoctorForm.vue"),
  },
];
