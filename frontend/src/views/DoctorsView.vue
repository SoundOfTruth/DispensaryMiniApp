<template>
  <div class="doctors-list" v-if="doctors?.length">
    <div v-if="doctors?.length == 0">В базе нет врачей</div>
    <DoctorCard v-else :doctor="doctor" v-for="doctor in doctors"></DoctorCard>
  </div>
  <div class="err-handler" v-else-if="err">{{ err }}</div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import DoctorCard from "../components/DoctorCard.vue";

import { useDoctorStore } from "../stores/DoctorStore";

const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);
const err = computed(() => doctorStore.err);

onMounted(async () => {
  await doctorStore.loadDoctors();
});
</script>

<style scoped lang="scss">
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 16px;
}
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
