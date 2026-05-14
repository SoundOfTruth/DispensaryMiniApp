import DefaultLayout from "../layouts/DefaultLayout.vue";

import type { RouteRecordRaw } from "vue-router";

export const publicRoutes: RouteRecordRaw = {
  path: "/",
  component: DefaultLayout,
  children: [
    {
      path: "/",
      name: "index",
      component: () => import("@/views/public/IndexView.vue"),
    },
    {
      path: "/doctors",
      name: "doctors",
      component: () => import("@/views/public/doctors/ListView.vue"),
    },
    {
      path: "/doctors/:doctorId(\\d+)",
      name: "doctors.detail",
      component: () => import("@/views/public/doctors/DetailView.vue"),
    },
    {
      path: "/inspections",
      name: "inspections",
      component: () => import("@/views/public/inspections/ListView.vue"),
    },
    {
      path: "/inspections/:inspectionId(\\d+)",
      name: "inspections.detail",
      component: () => import("@/views/public/inspections/DetailView.vue"),
    },
    {
      path: "/equipments",
      name: "equipments",
      component: () => import("@/views/public/EquipmentsView.vue"),
    },
    {
      path: "/logout",
      name: "logout",
      component: () => import("@/views/public/LogoutView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "notFound",
      props: { urlName: "index" },
      component: () => import("@/views/NotFoundView.vue"),
    },
  ],
};
