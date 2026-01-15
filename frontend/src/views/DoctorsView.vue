<template>
  <div class="doctors-list">
    <DoctorCard :doctor="doctor" v-for="doctor in doctors"></DoctorCard>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import DoctorCard from "../components/DoctorCard.vue";
import DoctorsApi from "../api/doctors";
import type { SimpleDoctor } from "../types/doctors";

const doctors = ref<SimpleDoctor[]>();

onMounted(async () => {
  doctors.value = await DoctorsApi.getAll();
});
</script>

<style scoped lang="scss">
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
