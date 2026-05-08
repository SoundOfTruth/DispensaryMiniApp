<template>
  <div class="modal" v-if="props.open">
    <div class="modal-container">
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
    <div class="modal-backdrop" @click="emits('close')"></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  open: boolean;
}>();

const emits = defineEmits(["close"]);
</script>

<style lang="scss" scoped>
.modal {
  z-index: 101;
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  .modal-container {
    z-index: 100;
  }
}
.modal-content {
  background: white;
  padding-inline: 20px;
  padding-bottom: 20px;
  background: white;
  border-radius: 16px;
  width: 320px;
  .modal-content {
    padding: 10px;
    text-align: center;
  }
}

.modal-backdrop {
  z-index: 99;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  opacity: 0.5;
}
</style>
