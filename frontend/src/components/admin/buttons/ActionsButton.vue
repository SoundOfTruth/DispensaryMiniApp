<template>
  <div>
    <button class="drowdown" @click="isOpen = !isOpen">Действия</button>
    <div v-if="isOpen">
      <button class="btn" @click="deleteItems()">Удалить выбранное</button>
      <div class="modal-backdrop" @click="isOpen = !isOpen"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const emits = defineEmits(["delete"]);

const isOpen = ref<boolean>(false);

const deleteItems = () => {
  isOpen.value = false;
  emits("delete");
};
</script>

<style lang="scss" scoped>
.modal-backdrop {
  z-index: 99;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
}
.drowdown {
  z-index: 100;
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
  z-index: 100;
}
</style>
