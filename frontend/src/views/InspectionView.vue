<template>
  <div>
    <div class="information">
      <div class="title">{{ research?.title }}</div>
      <div class="sub-title">Описание:</div>
      <div class="text">{{ research?.description }}</div>
      <div class="sub-title">Подготовка к иследованию:</div>
      <div class="text">{{ research?.preparation }}</div>
      <div class="sub-title">Проводит исследование:</div>
      <RouterLink :to="`/doctors/${research?.doctor.id}`">{{
        doctor?.fullname
      }}</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { getInspectionsJsonPayload } from "../types/inspections";
import { getDoctorPayload } from "../types/doctors";
const route = useRoute();
const researchId = Number(route.params.researchId) - 1;
const research = getInspectionsJsonPayload()[researchId];
const doctor = getDoctorPayload(research?.doctor);
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
