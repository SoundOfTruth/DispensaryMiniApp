<template>
  <div class="err-handler" v-if="errCondition">{{ err }}</div>
  <div class="container" v-else>
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
import InspectionCard from "../components/inspections/InspectionCard.vue";
import SearchField from "../components/SearchField.vue";

import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import { useInspectionStore } from "../stores/InspectionStore";

const route = useRoute();
const inspectionStore = useInspectionStore();
const inspections = computed(() => inspectionStore.inspections);
const err = computed(() => inspectionStore.err);
const errCondition = computed(
  () => inspections.value == undefined || inspections.value?.length == 0,
);
onMounted(async () => {
  await inspectionStore.loadInspections();
});

watch(
  () => route.query,
  async () => {
    await inspectionStore.loadInspections();
  },
);
</script>

<style lang="scss" scoped>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
  .inspections-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    padding: 0px 15px;
  }
}
</style>
