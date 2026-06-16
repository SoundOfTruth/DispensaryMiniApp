<template>
  <AdaptivePage>
    <div class="inspections-page">
      <div class="filters">
        <SearchField title="Поиск обследований" />
      </div>
      <PaginatedPage :count="inspectionStore.count">
        <div class="err-handler" v-for="err in errors" v-if="errCondition">
          {{ err.message }}
        </div>
        <div class="inspections-list">
          <InspectionCard :inspection="inspection" v-for="inspection in inspections" />
        </div>
      </PaginatedPage>
    </div>
  </AdaptivePage>
</template>

<script setup lang="ts">
import AdaptivePage from '@/components/AdaptivePage.vue';
import SearchField from '@/components/SearchField.vue';
import PaginatedPage from '@/components/PaginatedPage.vue';
import InspectionCard from '@/components/inspections/InspectionCard.vue';

import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

import { useInspectionStore } from '@/stores/inspections';
import { useErrorStore } from '@/stores/errors';
import { usePaginationStore } from '@/stores/paginationStore';

const route = useRoute();

const errorStore = useErrorStore();
const inspectionStore = useInspectionStore();
const paginationStore = usePaginationStore();

const inspections = computed(() => inspectionStore.inspections);
const errors = computed(() => errorStore.errors);
const errCondition = computed(
  () => inspections.value === undefined || inspections.value?.length == 0
);

const afterLoad = () => {
  const search = route.query.search;
  if (inspections.value.length === 0 && errors.value.length === 0) {
    if (!search) {
      errorStore.setErrorMessage('Ничего не найдено...');
    } else {
      errorStore.setErrorMessage('Ничего не найдено по заданным параметрам.');
    }
  }
};

onMounted(async () => {
  paginationStore.setLimit(5);
  await inspectionStore.loadPublicList();
  afterLoad();
});

watch(
  () => route.query,
  async () => {
    await inspectionStore.loadPublicList();
    afterLoad();
  }
);
</script>

<style lang="scss" scoped>
.inspections-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  .inspections-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
}
.err-handler {
  display: flex;
  justify-content: center;
  font-weight: 500;
  color: #ef4444;
}
.filters {
  padding-bottom: 20px;
  display: flex;
  gap: 10px;
}
</style>
