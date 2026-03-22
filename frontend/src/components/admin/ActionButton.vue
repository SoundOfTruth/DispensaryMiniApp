<template>
  <div>
    <button class="drowdown" @click="isOpen = !isOpen">Действия</button>
    <div v-if="isOpen">
      <button class="btn">Удалить выбранное</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const isOpen = ref<boolean>(false);
</script>

<style lang="scss" scoped>
.drowdown {
  background: #f8fafc;
  &:hover {
    border-color: transparent !important;
  }
  &:focus,
  &:focus-visible {
    outline: none !important;
  }
}
.btn {
  background: white;
  border: 1px solid gray;
  border-radius: 4px;
  position: absolute;
  box-sizing: border-box;
}
</style>
