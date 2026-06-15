<template>
  <div v-if="props.open" class="modal-overlay" @click="emits('close')">
    <div class="modal-content" @click.stop>
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  open: boolean;
}>();

const emits = defineEmits(['close']);
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--bg-primary);
  border-radius: 16px;
  width: 90%;
  max-width: 450px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
