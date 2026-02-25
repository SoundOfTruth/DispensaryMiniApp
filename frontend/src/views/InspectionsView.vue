<template>
  <div class="err-handler" v-if="errCondition">{{ err }}</div>
  <div v-else>
    <SearchField title="Поиск обследований" />
    <div class="inspections-list">
      <InspectionCard
        :inspection="inspection"
        v-for="inspection in inspections"
      ></InspectionCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import InspectionCard from "../components/InspectionCard.vue";
import SearchField from "../components/SearchField.vue";
import { computed, onMounted } from "vue";

import { useInspectionStore } from "../stores/InspectionStore";

const inspectionStore = useInspectionStore();
const inspections = computed(() => inspectionStore.inspections);
const err = computed(() => inspectionStore.err);
const errCondition = computed(
  () => inspections.value == undefined || inspections.value?.length == 0,
);
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
