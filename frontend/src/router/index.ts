import { createWebHistory, createRouter } from "vue-router";

import DefaultLayout from "../layouts/DefaultLayout.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: DefaultLayout,
      children: [
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
    },
    {
      path: "/admin",
      component: () => import("../layouts/AdminLayout.vue"),
      children: [
        {
          path: "doctors",
          name: "admin.doctors",
          component: () => import("../views/admin/AdminDoctorView.vue"),
        },
        {
          path: "doctors/create",
          name: "admin.doctors.create",
          component: () => import("../views/admin/forms/DoctorsForm.vue"),
        },
        {
          path: "",
          name: "admin.index",
          component: () => import("../views/admin/AdminView.vue"),
        },
      ],
    },
  ],
});

router.beforeEach((to, _from, next) => {
  const pageQuery = to.query.page;
  const page = Number(pageQuery);
  if (pageQuery && (page < 1 || isNaN(page))) {
    next({
      ...to,
      query: { ...to.query, page: 1 },
    });
  } else {
    next();
  }
});
