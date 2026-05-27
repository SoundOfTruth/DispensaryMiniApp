<template>
  <div class="form-container">
    <form @keydown.enter.prevent @submit.prevent="emits('submit')">
      <slot />
    </form>
    <Teleport to="#modals">
      <AdminErrorModal :errors="errorStore.errors" @close="errorStore.clearErrors()" />
    </Teleport>
  </div>
</template>

<script lang="ts" setup>
import { useErrorStore } from '@/stores/errors';
import AdminErrorModal from '../modals/AdminErrorModal.vue';

const errorStore = useErrorStore();

const emits = defineEmits(['submit']);
</script>

<style lang="scss" scoped>
.form-container {
  max-width: 600px;
  width: 100%;
  padding: 20px;
  margin-left: 10%;
  box-sizing: border-box;
  overflow: hidden;

  @media (max-width: 500px) {
    margin: 0px;
  }
}
</style>
