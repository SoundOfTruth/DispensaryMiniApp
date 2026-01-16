<template>
  <div class="form-list" v-if="activeForm === null">
    <div @click="openForm(ActiveForm.inspectionsForm)">
      Форма добавления обследования
    </div>
    <div @click="openForm(ActiveForm.doctorsForm)">Форма добавления врача</div>
  </div>
  <div v-if="activeForm == ActiveForm.inspectionsForm">
    <InspectionForm
      :available-doctors="doctors"
      @cancel="cancel"
    ></InspectionForm>
  </div>
  <div v-if="activeForm == ActiveForm.doctorsForm">
    <DoctorsForm @cancel="cancel"></DoctorsForm>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import DoctorsApi from "../api/doctors";
import type { SimpleDoctor } from "../types/doctors";
import InspectionForm from "../components/InspectionForm.vue";
import DoctorsForm from "../components/DoctorsForm.vue";

const ActiveForm = {
  inspectionsForm: 0,
  doctorsForm: 1,
};

type ActiveFormSwitch = (typeof ActiveForm)[keyof typeof ActiveForm];
const activeForm = ref<number | null>(null);

const openForm = (form: ActiveFormSwitch) => {
  switch (form) {
    case ActiveForm.inspectionsForm:
      activeForm.value = ActiveForm.inspectionsForm;
      break;
    case ActiveForm.doctorsForm:
      activeForm.value = ActiveForm.doctorsForm;
      break;
  }
};

const cancel = () => {
  activeForm.value = null;
};

const doctors = ref<SimpleDoctor[]>([]);

onMounted(async () => {
  try {
    doctors.value = await DoctorsApi.getAll();
  } catch (error) {
    console.error("Failed to load doctors:", error);
  }
});
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
