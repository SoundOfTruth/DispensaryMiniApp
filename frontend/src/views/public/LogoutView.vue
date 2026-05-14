<template>
  <div class="logout-view">
    <h2>Выход из системы...</h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/users";

const router = useRouter();
const userStore = useUserStore();

onMounted(async () => {
  await userStore.logout();
  await router.push({ name: "index" });
});
</script>
