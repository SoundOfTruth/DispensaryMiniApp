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
import { getInspectionsJsonPayload } from "../types/inspections";

const inspections = getInspectionsJsonPayload();
</script>

<style lang="scss" scoped>
.inspections-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
