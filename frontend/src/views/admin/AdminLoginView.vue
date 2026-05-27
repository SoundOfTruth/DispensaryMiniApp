<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue';

import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/users';
import { useErrorStore } from '@/stores/errors';

const router = useRouter();

const userStore = useUserStore();
const errorStore = useErrorStore();

const afterSubmit = async () => {
  await userStore.loadCurrentUser();
  if (userStore.isAdmin) {
    router.push({ name: 'admin.index' });
  } else if (userStore.currentUser && errorStore.errors.length === 0) {
    errorStore.addErrorMessage('Недостаточно прав.');
  }
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
