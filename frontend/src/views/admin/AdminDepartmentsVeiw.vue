<template>
  <AdminPage
    title="Отделения"
    add-button-name="Добавить отделение"
    :columns="columns"
    :data="store.departments"
    :store="store"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useDepartmentStore } from "@/stores/departments";

import { type Department } from "@/types/departments";

interface Columns {
  key: keyof Department;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "name", text: "Название" },
];

const store = useDepartmentStore();
</script>
