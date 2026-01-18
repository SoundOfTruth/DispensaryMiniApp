<template>
  <div class="doctors-list">
    <DoctorCard :doctor="doctor" v-for="doctor in doctors"></DoctorCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import DoctorCard from "../components/DoctorCard.vue";

import { useDoctorStore } from "../stores/DoctorStore";

const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);

onMounted(async () => {
  await doctorStore.loadDoctors();
});
</script>

<style scoped lang="scss">
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
