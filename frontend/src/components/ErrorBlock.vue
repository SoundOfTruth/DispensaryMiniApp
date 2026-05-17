<template>
  <div class="errors-block">
    <div
      v-for="(error, index) in errorStore.errors"
      :key="index"
      class="error-message"
    >
      {{ error.message }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.errors-block{
  padding-left: 4px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.error-message {
  display: block;
  margin-top: 0.5rem;
  color: #e74c3c;
  font-size: 0.8rem;
}
</style>

<script setup lang="ts">
import { useErrorStore } from "@/stores/errors";

const errorStore = useErrorStore();
</script>
