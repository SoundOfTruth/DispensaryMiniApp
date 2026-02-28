<template>
  <button class="filter-btn" @click="filterOpen = !filterOpen">
    <FilterSvg />
  </button>
  <div>
    <Teleport to="#modals">
      <FilterModal :open="filterOpen" @close="filterOpen = false" />
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import FilterSvg from "./svg/FilterSvg.vue";
import FilterModal from "./modals/DoctorFilterModal.vue";

import { ref } from "vue";
const filterOpen = ref<boolean>(false);
</script>

<style lang="scss" scoped>
.filter-btn {
  padding: 0;
  display: flex;
  align-items: center;
  background: transparent;
}
</style>
