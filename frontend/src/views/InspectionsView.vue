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
import { ref, onMounted } from "vue";

import InspectionsApi from "../api/inspections";
import type { Inspection } from "../types/inspections";


const inspections = ref<Inspection[]>();

onMounted(async () => {
  inspections.value = await InspectionsApi.getInspections();
});
</script>

<style lang="scss" scoped>
.inspections-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
