<template>
  <AdminPage
    title="Пользователи"
    add-button-name="Добавить пользователя"
    :columns="columns"
    :data="store.users"
    :store="store"
  />
</template>

<script lang="ts" setup>
import AdminPage from "@/components/admin/AdminPage.vue";

import { useUserStore } from "@/stores/users";

import { type User } from "@/types/users";

interface Columns {
  key: keyof User;
  text: string;
}

const columns: Columns[] = [
  { key: "id", text: "id" },
  { key: "email", text: "Почта" },
  { key: "lastname", text: "Фамилия" },
  { key: "firstname", text: "Имя" },
  { key: "middlename", text: "Отчество" },
  { key: "role", text: "Роль" },
];

const store = useUserStore();
</script>
