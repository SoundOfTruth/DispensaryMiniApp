<template>
  <AdminPage
    title="Специальности"
    add-button-name="Добавить специальность"
    :columns="columns"
    :data="store.specialties"
    :store="store"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useSpecialityStore } from "@/stores/specialties";

import { type Speciality } from "@/types/specialities";

interface Columns {
  key: keyof Speciality;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "name", text: "Название" },
];

const store = useSpecialityStore();
</script>
