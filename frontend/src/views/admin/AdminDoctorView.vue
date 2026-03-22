<template>
  <AdminPage
    title="Врачи"
    add-button-name="Добавить врача"
    :columns="columns"
    :data="doctors"
    :store="doctorStore"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";

import { useDoctorStore } from "@/stores/DoctorStore";
import type { SimpleDoctor } from "@/types/doctors";

const route = useRoute();
const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);

interface Columns {
  key: keyof SimpleDoctor;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "lastname", text: "Фамилия" },
  { key: "firstname", text: "Имя" },
  { key: "middlename", text: "Отчество" },
];

interface inputData {
  title?: string;
}
const props = defineProps<inputData>();

onMounted(async () => {
  await doctorStore.loadList();
});

watch(
  () => route.query,
  async () => {
    await doctorStore.loadList();
  },
  { deep: true },
);
</script>
