import { createWebHistory, createRouter } from "vue-router";

import IndexView from "../views/IndexView.vue";
import DoctorsView from "../views/DoctorsView.vue";
import DoctorView from "../views/DoctorView.vue";
import InspectionsView from "../views/InspectionsView.vue";
import InspectionView from "../views/InspectionView.vue";
import AdminView from "../views/AdminView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import EquipmentsView from "../views/EquipmentsView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/admin", name: "admin", component: AdminView },
    { path: "/", name: "index", component: IndexView },
    { path: "/doctors", name: "doctors", component: DoctorsView },
    { path: "/doctors/:doctorId(\\d+)", name: "doctor", component: DoctorView },
    { path: "/inspections", name: "inspections", component: InspectionsView },
    {
      path: "/inspections/:inspectionId(\\d+)",
      name: "inspection",
      component: InspectionView,
    },
    { path: "/equipments", name: "equipments", component: EquipmentsView },
    { path: "/:pathMatch(.*)*", name: "notFound", component: NotFoundView },
  ],
});
