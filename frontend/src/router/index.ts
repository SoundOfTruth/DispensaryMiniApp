import { createWebHistory, createRouter } from "vue-router";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/admin",
      name: "admin",
      component: () => import("../views/AdminView.vue"),
    },
    {
      path: "/",
      name: "index",
      component: () => import("../views/IndexView.vue"),
    },
    {
      path: "/doctors",
      name: "doctors",
      component: () => import("../views/DoctorsView.vue"),
    },
    {
      path: "/doctors/:doctorId(\\d+)",
      name: "doctor",
      component: () => import("../views/DoctorView.vue"),
    },
    {
      path: "/inspections",
      name: "inspections",
      component: () => import("../views/InspectionsView.vue"),
    },
    {
      path: "/inspections/:inspectionId(\\d+)",
      name: "inspection",
      component: () => import("../views/InspectionView.vue"),
    },
    {
      path: "/equipments",
      name: "equipments",
      component: () => import("../views/EquipmentsView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "notFound",
      component: () => import("../views/NotFoundView.vue"),
    },
  ],
});
