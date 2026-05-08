<template>
  <AdminPage
    title="Обследования"
    add-button-name="Добавить обследование"
    :columns="columns"
    :data="store.inspections"
    :store="store"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useInspectionStore } from "@/stores/inspections";

import type { SimpleInspection } from "@/types/inspections";

interface Columns {
  key: keyof SimpleInspection;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "title", text: "Название" },
];

const store = useInspectionStore();
</script>
