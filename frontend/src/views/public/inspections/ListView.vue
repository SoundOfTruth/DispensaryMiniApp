<template>
  <div id="scroll-container" class="container">
    <div class="filters">
      <SearchField title="Поиск обследований" />
    </div>
    <PaginatedPage
      :count="inspectionStore.count"
      :limit="inspectionStore.limit"
    >
      <div class="err-handler" v-for="err in errors" v-if="errCondition">
        {{ err.message }}
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

import { useInspectionStore } from "@/stores/inspections";

const route = useRoute();
const inspectionStore = useInspectionStore();
const inspections = computed(() => inspectionStore.inspections);
const errors = computed(() => inspectionStore.errors);
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
.err-handler {
  display: flex;
  justify-content: center;
}
.filters {
  padding-top: 20px;
  padding-inline: 25px;
  padding-bottom: 20px;
  display: flex;
  gap: 10px;
}
</style>
