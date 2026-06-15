<template>
  <div class="inspection-page">
    <div
      class="err-handler"
      v-for="err in errors"
      v-if="!inspection || inspection.id !== inspectionId"
    >
      {{ err.message }}
    </div>
    <div v-else>
      <div class="inspection-card">
        <div class="title">{{ inspection?.title }}</div>
        <div class="sub-title" v-if="inspection?.description">Описание:</div>
        <div class="text">{{ inspection?.description }}</div>
        <div class="sub-title" v-if="inspection?.preparation">Подготовка к иследованию:</div>
        <div class="text">{{ inspection?.preparation }}</div>
        <div class="sub-title" v-if="inspection?.doctors.length">Проводят исследование:</div>
        <div>
          <div v-for="doctor in inspection?.doctors">
            <RouterLink :to="`/doctors/${doctor.id}`" class="doctor-link">{{
              `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`
            }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

import { useInspectionStore } from '@/stores/inspections';
import { useErrorStore } from '@/stores/errors';

const route = useRoute();
const inspectionId = Number(route.params.inspectionId);

const inspectionStore = useInspectionStore();
const errorStore = useErrorStore();

const inspection = computed(() => inspectionStore.inspection);
const errors = computed(() => errorStore.errors);

onMounted(async () => {
  await inspectionStore.loadById(inspectionId);
});
</script>

<style scoped lang="scss">
.inspection-page {
  background: var(--bg-secondary);
  overflow-y: auto;
  margin: 15px;
}
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 110%;
  text-align: center;
}
.inspection-card {
  display: flex;
  gap: 10px;
  flex-direction: column;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  .title {
    font-weight: 500;
    font-size: 150%;
  }
  .sub-title {
    font-size: 110%;
    color: #b1b2b4;
    line-height: 1;
  }
  .text {
    white-space: pre-wrap;
  }
}
.doctor-link {
  color: #0d9ce3;
}
</style>
