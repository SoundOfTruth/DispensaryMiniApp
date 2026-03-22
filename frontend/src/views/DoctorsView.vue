<template>
  <div id="scroll-container" class="container">
    <SearchField title="Поиск врачей"
      ><template #filter> <FilterButton /></template
    ></SearchField>
    <PaginatedPage :count="doctorStore.count" :limit="doctorStore.limit">
      <div class="err-handler" v-if="errCondition">
        {{ err }}
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

import { useDoctorStore } from "@/stores/DoctorStore";

const route = useRoute();
const doctorStore = useDoctorStore();
const doctors = computed(() => doctorStore.doctors);
const err = computed(() => doctorStore.err);
const errCondition = computed(
  () => doctors.value == undefined || doctors.value?.length == 0,
);

onMounted(async () => {
  await doctorStore.loadList();
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
    overflow-y: auto;
    padding: 0px 15px;
  }
}
</style>
