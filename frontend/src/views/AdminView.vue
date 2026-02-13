<template>
  <div>
    <div class="form-list" v-if="activeForm === null">
      <div @click="openForm(ActiveForm.inspectionsForm)">
        Форма создания обследования
      </div>
      <div @click="openForm(ActiveForm.doctorsForm)">Форма создания врача</div>
      <div @click="openForm(ActiveForm.specialitiesForm)">
        Форма создания специальности
      </div>
      <div @click="openForm(ActiveForm.departmentsForm)">
        Форма создания отделения
      </div>
    </div>
    <div v-if="activeForm == ActiveForm.inspectionsForm">
      <InspectionForm :doctors="doctors" @cancel="cancel"></InspectionForm>
    </div>
    <div v-if="activeForm == ActiveForm.doctorsForm">
      <DoctorsForm
        :departments="departments"
        :specialities="specialities"
        @cancel="cancel"
      ></DoctorsForm>
    </div>
    <div v-if="activeForm == ActiveForm.specialitiesForm">
      <SpecialityForm @cancel="cancel"></SpecialityForm>
    </div>
    <div v-if="activeForm == ActiveForm.departmentsForm">
      <DepartmentForm @cancel="cancel"></DepartmentForm>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from "vue";

import InspectionForm from "../components/InspectionForm.vue";
import DoctorsForm from "../components/DoctorsForm.vue";
import SpecialityForm from "../components/SpecialityForm.vue";

import { useDoctorStore } from "../stores/DoctorStore";
import { useDepartmentStore } from "../stores/DepartmentStore";
import { useSpecialityStore } from "../stores/SpecialityStore";
import DepartmentForm from "../components/DepartmentForm.vue";

const DoctorStore = useDoctorStore();
const DepartmentStore = useDepartmentStore();
const SpecialitiesStore = useSpecialityStore();
const doctors = computed(() => DoctorStore.doctors);
const departments = computed(() => DepartmentStore.departments);
const specialities = computed(() => SpecialitiesStore.specialities);

onMounted(async () => {
  await DoctorStore.loadDoctors();
  await DepartmentStore.loadDepartments();
  await SpecialitiesStore.loadSpecialities();
});

const ActiveForm = {
  inspectionsForm: 0,
  doctorsForm: 1,
  specialitiesForm: 2,
  departmentsForm: 3,
};

type ActiveFormSwitch = (typeof ActiveForm)[keyof typeof ActiveForm];
const activeForm = ref<number | null>(null);

const openForm = (form: ActiveFormSwitch) => {
  activeForm.value = form;
};

const cancel = () => {
  activeForm.value = null;
};
</script>

<style scoped lang="scss">
.form-list {
  display: flex;
  flex-direction: column;
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
</style>
