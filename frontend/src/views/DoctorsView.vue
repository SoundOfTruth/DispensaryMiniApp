<template>
  <div class="doctors-list">
    <DoctorCard :doctor="doctor" v-for="doctor in doctors"></DoctorCard>
  </div>
</template>

<script setup lang="ts">
import DoctorCard from "../components/DoctorCard.vue";
import { getDoctorsJsonPayload } from "../types/doctors";

const doctors = getDoctorsJsonPayload();
</script>

<style scoped lang="scss">
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
