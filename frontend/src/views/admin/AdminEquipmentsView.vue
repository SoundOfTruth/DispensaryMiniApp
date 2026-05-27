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
import AdminPage from '@/components/admin/AdminPage.vue';

import { useEquipmentStore } from '@/stores/equipments';

import type { Equipment, SimpleEquipmentType } from '@/types/equipments';

interface Columns {
  key: keyof Equipment;
  text: string;
  secondKey?: keyof SimpleEquipmentType;
}

const columns: Columns[] = [
  { key: 'id', text: 'id' },
  { key: 'name', text: 'Название' },
  { key: 'type', text: 'Тип', secondKey: 'name' },
];

const equipmentStore = useEquipmentStore();
</script>
