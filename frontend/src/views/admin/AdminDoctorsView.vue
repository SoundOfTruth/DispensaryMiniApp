<template>
  <AdminPage
    title="Врачи"
    add-button-name="Добавить врача"
    :columns="columns"
    :data="doctorStore.doctors"
    :store="doctorStore"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useDoctorStore } from "@/stores/doctors";
import type { Department } from "@/types/departments";

import type { SimpleDoctor } from "@/types/doctors";
import type { Speciality } from "@/types/specialities";

interface Columns {
  key: keyof SimpleDoctor;
  text: string;
  secondKey?: keyof Speciality | keyof Department;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "lastname", text: "Фамилия" },
  { key: "firstname", text: "Имя" },
  { key: "middlename", text: "Отчество" },
  { key: "speciality", text: "Специальность", secondKey: "name" },
  { key: "department", text: "Отделение", secondKey: "name" },
];

const doctorStore = useDoctorStore();
</script>
