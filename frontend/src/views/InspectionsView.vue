<template>
  <div class="inspections-list" v-if="inspections?.length">
    <div v-if="inspections?.length == 0">В базе нет обследований</div>
    <InspectionCard
      v-else
      :inspection="inspection"
      v-for="inspection in inspections"
    ></InspectionCard>
  </div>
  <div class="err-handler" v-else-if="err">{{ err }}</div>
</template>

<script setup lang="ts">
import InspectionCard from "../components/InspectionCard.vue";
import { computed, onMounted } from "vue";

import { useInspectionStore } from "../stores/InspectionStore";

const inspectionStore = useInspectionStore();
const inspections = computed(() => inspectionStore.inspections);
const err = computed(() => inspectionStore.err);
onMounted(async () => {
  await inspectionStore.loadInspections();
});
</script>

<style lang="scss" scoped>
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 16px;
}
.inspections-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
