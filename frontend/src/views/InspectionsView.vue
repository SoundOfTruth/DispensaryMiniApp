<template>
  <div id="scroll-container" class="container">
    <SearchField title="Поиск обследований" />
    <PaginatedPage
      :count="inspectionStore.count"
      :limit="inspectionStore.limit"
    >
      <div class="err-handler" v-if="errCondition">
        {{ err }}
      </div>
      <div class="inspections-list">
        <InspectionCard
          :inspection="inspection"
          v-for="inspection in inspections"
        />
      </div>
    </PaginatedPage>
  </div>
</template>

<script setup lang="ts">
import SearchField from "@/components/SearchField.vue";
import PaginatedPage from "@/components/PaginatedPage.vue";
import InspectionCard from "@/components/inspections/InspectionCard.vue";

import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import { useInspectionStore } from "@/stores/InspectionStore";

const route = useRoute();
const inspectionStore = useInspectionStore();
const inspections = computed(() => inspectionStore.inspections);
const err = computed(() => inspectionStore.err);
const errCondition = computed(
  () => inspections.value == undefined || inspections.value?.length == 0,
);
onMounted(async () => {
  await inspectionStore.loadList();
});

watch(
  () => route.query,
  async () => {
    await inspectionStore.loadList();
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
