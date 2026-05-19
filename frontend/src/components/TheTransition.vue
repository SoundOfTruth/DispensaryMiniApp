<template>
  <Transition name="fade" mode="out-in">
    <slot></slot>
  </Transition>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<script lang="ts" setup>
import { Transition } from "vue";
</script>
