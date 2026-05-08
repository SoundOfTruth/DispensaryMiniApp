import type { RouteRecordRaw } from "vue-router";

export const userRoutes: RouteRecordRaw[] = [
  {
    path: "user",
    name: "admin.users",
    component: () => import("@/views/admin/AdminUsersView.vue"),
  },
  {
    path: "users/create",
    name: "admin.users.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/UserForm.vue"),
  },
  {
    path: "users/:id(\\d+)/edit",
    name: "admin.users.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/UserForm.vue"),
  },
  {
    path: "users/:id(\\d+)",
    name: "admin.users.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/UserForm.vue"),
  },
];
