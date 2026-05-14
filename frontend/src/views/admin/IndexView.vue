<template>
  <div>Панель администратора</div>
  <div>{{ userStore.currentUser }}</div>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/stores/users";

const userStore = useUserStore();
</script>
