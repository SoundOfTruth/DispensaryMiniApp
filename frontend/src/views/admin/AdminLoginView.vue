<script setup lang="ts">
import LoginForm from "@/components/LoginForm.vue";

import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/users";

const router = useRouter();
const userStore = useUserStore();

const afterSubmit = async () => {
  await userStore.loadCurrentUser();
  router.push({ name: "admin.index" });
};
</script>

<template>
  <div class="login-page">
    <div class="title">Вход в личный кабинет</div>
    <div class="test">
      <LoginForm @after-submit="afterSubmit" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  padding-top: 14vh;
  display: flex;
  flex-direction: column;
  place-content: center;
  align-items: center;
}
.title {
  font-size: 140%;
}
.test {
  width: 302px;
  padding-top: 20px;
}
</style>
