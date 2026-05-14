import type { RouteRecordRaw } from "vue-router";
import { doctorsRoute } from "./admin/doctors";
import { inspectionsRoute } from "./admin/inspections";
import { specialityRoutes } from "./admin/specialties";
import { departmentRoutes } from "./admin/departments";
import { equipmentRoutes } from "./admin/equipments";
import { userRoutes } from "./admin/users";
import { equipmentTypesRoutes } from "./admin/equipmentTypes";

export const adminRoutes: RouteRecordRaw = {
  path: "/admin",
  component: () => import("@/layouts/AdminLayout.vue"),
  children: [
    ...doctorsRoute,
    ...inspectionsRoute,
    ...specialityRoutes,
    ...departmentRoutes,
    ...equipmentRoutes,
    ...userRoutes,
    ...equipmentTypesRoutes,
    {
      path: "",
      name: "admin.index",
      component: () => import("@/views/admin/IndexView.vue"),
    },
    {
      path: "login",
      name: "admin.login",
      component: () => import("@/views/admin/AdminLoginView.vue"),
    },
    {
      path: ":pathMatch(.*)*",
      name: "admin.notFound",
      props: { urlName: "admin.index" },
      component: () => import("@/views/NotFoundView.vue"),
    },
  ],
};
