import type { RouteRecordRaw } from "vue-router";

export const inspectionsRoute: RouteRecordRaw[] = [
  {
    path: "inspections",
    name: "admin.inspections",
    component: () => import("@/views/admin/AdminInspectionsView.vue"),
  },
  {
    path: "inspections/create",
    name: "admin.inspections.create",
    props: { mode: "create" },
    component: () => import("@/components/admin/forms/InspectionForm.vue"),
  },
  {
    path: "inspections/:id(\\d+)/edit",
    name: "admin.inspections.edit",
    props: { mode: "edit" },
    component: () => import("@/components/admin/forms/InspectionForm.vue"),
  },
  {
    path: "inspections/:id(\\d+)",
    name: "admin.inspections.detail",
    props: { mode: "detail" },
    component: () => import("@/components/admin/forms/InspectionForm.vue"),
  },
];
