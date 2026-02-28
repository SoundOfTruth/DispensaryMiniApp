<template>
  <div class="inspection-page">
    <div class="err-handler" v-if="!inspection">{{ inspectionStore.err }}</div>
    <div v-else>
      <div class="information">
        <div class="title">{{ inspection?.title }}</div>
        <div class="sub-title" v-if="inspection?.description">Описание:</div>
        <div class="text">{{ inspection?.description }}</div>
        <div class="sub-title" v-if="inspection?.preparation">
          Подготовка к иследованию:
        </div>
        <div class="text">{{ inspection?.preparation }}</div>
        <div class="sub-title" v-if="inspection?.doctors.length">
          Проводят исследование:
        </div>
        <div>
          <div v-for="doctor in inspection?.doctors">
            <RouterLink :to="`/doctors/${doctor.id}`">{{
              `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`
            }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useRoute } from "vue-router";

import { useInspectionStore } from "../stores/InspectionStore";

const inspectionStore = useInspectionStore();
const inspection = computed(() => inspectionStore.inspection);

const route = useRoute();

onMounted(async () => {
  const inspectionId = Number(route.params.inspectionId);
  await inspectionStore.loadInspection(inspectionId);
});
</script>

<style scoped lang="scss">
.inspection-page {
  padding: 0px 15px;
}
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 110%;
}
.information {
  display: flex;
  gap: 10px;
  flex-direction: column;
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
</style>
