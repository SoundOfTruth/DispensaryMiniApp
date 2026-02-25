<template>
  <div class="err-handler" v-if="errCondition">
    {{ err }}
  </div>
  <div v-else>
    <SearchField title="Поиск врачей" />
    <div class="doctors-list" v-if="doctors?.length">
      <DoctorCard :doctor="doctor" v-for="doctor in doctors" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import DoctorCard from "../components/DoctorCard.vue";

import { useDoctorStore } from "../stores/DoctorStore";
import SearchField from "../components/SearchField.vue";

const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);
const err = computed(() => doctorStore.err);
const errCondition = computed(
  () => doctors.value == undefined || doctors.value?.length == 0,
);

onMounted(async () => {
  await doctorStore.loadDoctors();
  console.log(doctors.value?.length);
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
