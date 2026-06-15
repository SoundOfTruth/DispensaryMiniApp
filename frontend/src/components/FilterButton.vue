<template>
  <button class="filter-btn" @click="emits('onClick')">
    <FilterSvg />
  </button>
</template>

<script setup lang="ts">
import FilterSvg from './svg/FilterSvg.vue';

const emits = defineEmits(['onClick']);
</script>

<style lang="scss" scoped>
.filter-btn {
  padding: 8px 12px;
  display: flex;
  align-items: center;
  background: var(--bg-secondary);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #3b82f6;


  &:active {
    transform: scale(0.98);
  }
}
</style>
