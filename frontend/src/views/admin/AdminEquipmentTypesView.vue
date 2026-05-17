<template>
  <AdminPage
    title="Типы оборудования"
    add-button-name="Добавить тип"
    :columns="columns"
    :data="typeStore.types"
    :store="typeStore"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useEquipmentTypeStore } from "@/stores/equipmentTypes";

import type { SimpleEquipmentType } from "@/types/equipments";

interface Columns {
  key: keyof SimpleEquipmentType;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "name", text: "Название" },
];

const typeStore = useEquipmentTypeStore();
</script>
