import type { RouteRecordRaw } from "vue-router";

export const equipmentTypesRoutes: RouteRecordRaw[] = [
  {
    path: "equipments-types",
    name: "admin.equipments-types",
    component: () => import("@/views/admin/AdminEquipmentTypesView.vue"),
  },
  {
    path: "equipments-types/create",
    name: "admin.equipments-types.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/EquipmentTypeForm.vue"),
  },
  {
    path: "equipments-types/:id(\\d+)/edit",
    name: "admin.equipments-types.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/EquipmentTypeForm.vue"),
  },
  {
    path: "equipments-types/:id(\\d+)",
    name: "admin.equipments-types.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/EquipmentTypeForm.vue"),
  },
];
