<template>
  <div class="container">
    <div class="filters">
      <SearchField title="Поиск врачей" />
      <FilterButton />
    </div>
    <PaginatedPage :count="doctorStore.count" :limit="doctorStore.limit">
      <div class="err-handler" v-for="err in errors" v-if="errCondition">
        {{ err.message }}
      </div>
      <div class="doctors-list">
        <DoctorCard :doctor="doctor" v-for="doctor in doctors" />
      </div>
    </PaginatedPage>
  </div>
</template>

<script setup lang="ts">
import SearchField from "@/components/SearchField.vue";
import FilterButton from "@/components/FilterButton.vue";
import PaginatedPage from "@/components/PaginatedPage.vue";
import DoctorCard from "@/components/doctors/DoctorCard.vue";

import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import { useDoctorStore } from "@/stores/doctors";

const route = useRoute();
const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);
const errors = computed(() => doctorStore.errors);
const errCondition = computed(
  () => doctors.value == undefined || doctors.value?.length == 0,
);

onMounted(() => {
  doctorStore.setLimit(8);
  doctorStore.loadList();
});

watch(
  () => route.query,
  async () => {
    await doctorStore.loadList();
  },
  { deep: true },
);
</script>

<style scoped lang="scss">
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 16px;
}
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
  .doctors-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0px 15px;
  }
}
.filters {
  padding-top: 20px;
  padding-inline: 25px;
  padding-bottom: 20px;
  display: flex;
  gap: 10px;
}
</style>
