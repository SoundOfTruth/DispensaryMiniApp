<template>
  <div class="form-container">
    <form @keydown.enter.prevent @submit.prevent="emits('submit')">
      <slot />
    </form>
  </div>
  <Teleport to="#modals">
    <AdminErrorModal :errors="store.errors" @close="store.errors = []" />
  </Teleport>
</template>

<script lang="ts" setup>
import AdminErrorModal from "../modals/AdminErrorModal.vue";
import type { BaseStore } from "@/stores/base";
const props = defineProps<{ store: BaseStore }>();
const emits = defineEmits(["submit"]);
</script>

<style lang="scss" scoped>
.form-container {
  max-width: 600px;
  padding: 20px;
  margin-left: 20%;
  @media (max-width: 500px) {
    margin: 0px;
  }
  
}
</style>
