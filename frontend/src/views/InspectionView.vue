<template>
  <div>
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
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import InspectionsApi from "../api/inspections";

import type { Inspection } from "../types/inspections";

const route = useRoute();
const inspection = ref<Inspection | null>(null);

onMounted(async () => {
  const inspectionId = Number(route.params.inspectionId);
  inspection.value = await InspectionsApi.get(inspectionId);
});
</script>

<style scoped lang="scss">
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
