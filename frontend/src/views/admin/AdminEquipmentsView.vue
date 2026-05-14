<template>
  <AdminPage
    title="Оборудование"
    add-button-name="Добавить оборудование"
    :columns="columns"
    :data="equipmentStore.equipments"
    :store="equipmentStore"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useEquipmentStore } from "@/stores/equipments";

import type { Equipment } from "@/types/equipments";

interface Columns {
  key: keyof Equipment;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "name", text: "Название" },
  { key: "type_id", text: "Тип" },
];

const equipmentStore = useEquipmentStore();
</script>
