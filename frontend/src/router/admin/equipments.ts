import type { RouteRecordRaw } from "vue-router";

export const equipmentRoutes: RouteRecordRaw[] = [
  {
    path: "equipments",
    name: "admin.equipments",
    component: () => import("@/views/admin/AdminEquipmentsView.vue"),
  },
  {
    path: "equipments/create",
    name: "admin.equipments.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/EquipmentForm.vue"),
  },
  {
    path: "equipments/:id(\\d+)/edit",
    name: "admin.equipments.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/EquipmentForm.vue"),
  },
  {
    path: "equipments/:id(\\d+)",
    name: "admin.equipments.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/EquipmentForm.vue"),
  },
];
