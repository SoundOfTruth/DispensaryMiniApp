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
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #3b82f6;

  &:hover {
    border-color: #3b82f6;
    background: #f0f9ff;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  }

  &:active {
    transform: scale(0.98);
  }
}
</style>
