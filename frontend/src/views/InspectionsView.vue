<template>
  <div class="inspections-list">
    <InspectionCard
      :inspection="inspection"
      v-for="inspection in inspections"
    ></InspectionCard>
  </div>
</template>

<script setup lang="ts">
import InspectionCard from "../components/InspectionCard.vue";
import { computed, onMounted } from "vue";

import { useInspectionStore } from "../stores/InspectionStore";

const InspectionStore = useInspectionStore();
const inspections = computed(() => InspectionStore.inspections);
onMounted(async () => {
  await InspectionStore.loadInspections();
});
</script>

<style lang="scss" scoped>
.inspections-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
