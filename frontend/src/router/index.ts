import { createWebHistory, createRouter } from "vue-router";

import IndexView from "../views/IndexView.vue";
import DoctorsView from "../views/DoctorsView.vue";
import DoctorView from "../views/DoctorView.vue";
import InspectionsView from "../views/InspectionsView.vue";
import InspectionView from "../views/InspectionView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: IndexView },
    { path: "/doctors", component: DoctorsView },
    { path: "/doctors/:doctorId(\\d+)", component: DoctorView },
    { path: "/inspections", component: InspectionsView },
    { path: "/inspections/:researchId(\\d+)", component: InspectionView },
  ],
});
