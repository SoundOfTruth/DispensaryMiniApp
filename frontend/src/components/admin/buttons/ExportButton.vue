<template>
  <div class="dropdown-container">
    <button class="dropdown" @click="isOpen = !isOpen">Экспорт</button>
    <div class="content" v-if="isOpen">
      <button class="btn">CSV</button>
      <button class="btn">JSON</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const isOpen = ref<boolean>(false);
</script>

<style lang="scss" scoped>
.dropdown-container {
  position: relative;
  display: inline-block;
}

.dropdown {
  background: #616876;
  color: white;
  border: 1px solid transparent;
  padding: 8px 16px;
  cursor: pointer;

  &:hover {
    border-color: #999 !important;
  }

  &:focus,
  &:focus-visible {
    outline: none;
  }
  @media (max-width: 720px) {
    display: none;
  }
}

.content {
  border: 1px solid gray;
  border-radius: 4px;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 100%;
  display: flex;
  flex-direction: column;
  z-index: 10;
  .btn {
    border: none;
    border-radius: 4px;
    background: white;
    padding: 8px 16px;
    cursor: pointer;
    white-space: nowrap;

    &:hover {
      background: #f0f0f0;
    }
  }
}
</style>
