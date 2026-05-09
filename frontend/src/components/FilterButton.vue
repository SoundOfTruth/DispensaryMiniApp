<template>
  <button class="filter-btn" @click="emits('onClick')">
    <FilterSvg />
  </button>
</template>

<script setup lang="ts">
import FilterSvg from "./svg/FilterSvg.vue";

const emits = defineEmits(["onClick"]);
</script>

<style lang="scss" scoped>
.filter-btn {
  padding: 0;
  display: flex;
  align-items: center;
  background: transparent;
}
</style>
