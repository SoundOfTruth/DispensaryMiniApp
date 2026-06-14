<template>
  <div class="container">
    <div class="filters">
      <SearchField title="Поиск врачей" />
      <FilterButton @on-click="filterOpen = !filterOpen" />
    </div>
    <div class="pt">
      <PaginatedPage :count="doctorStore.count">
        <div class="err-handler" v-for="err in errors" v-if="errCondition">
          {{ err.message }}
        </div>
        <div class="doctors-list">
          <DoctorCard :doctor="doctor" v-for="doctor in doctors" />
        </div>
      </PaginatedPage>
    </div>
    <Teleport to="#modals">
      <FilterModal :open="filterOpen" @close="filterOpen = false" />
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import FilterModal from '@/components/doctors/DoctorFilterModal.vue';
import SearchField from '@/components/SearchField.vue';
import FilterButton from '@/components/FilterButton.vue';
import PaginatedPage from '@/components/PaginatedPage.vue';
import DoctorCard from '@/components/doctors/DoctorCard.vue';

import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import { useDoctorStore } from '@/stores/doctors';

import { useErrorStore } from '@/stores/errors';
import { usePaginationStore } from '@/stores/paginationStore';

const filterOpen = ref<boolean>(false);

const route = useRoute();
const doctorStore = useDoctorStore();
const errorStore = useErrorStore();
const paginationStore = usePaginationStore();

const doctors = computed(() => doctorStore.doctors);
const errors = computed(() => errorStore.errors);
const errCondition = computed(() => doctors.value == undefined || doctors.value?.length == 0);

const afterLoad = () => {
  const search = route.query.search;
  if (doctors.value.length === 0 && errors.value.length === 0) {
    if (!search) {
      errorStore.setErrorMessage('Ничего не найдено...');
    } else {
      errorStore.setErrorMessage('Ничего не найдено по заданным параметрам.');
    }
  }
};

onMounted(async () => {
  paginationStore.setLimit(5);
  await doctorStore.loadList();
  afterLoad();
});

watch(
  () => [route.query],
  async () => {
    await doctorStore.loadList();
    afterLoad();
  },
  { deep: true }
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
    gap: 18px;
    padding: 0px 15px;
  }
}
.filters {
  position: sticky;
  top: 0px;
  padding-top: 20px;
  padding-inline: 25px;
  padding-bottom: 20px;
  display: flex;
  gap: 10px;
  background: #f5f7fa;
}
</style>
