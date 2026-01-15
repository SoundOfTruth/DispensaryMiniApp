<template>
  <div>
    <InspectionForm :available-doctors="doctors"></InspectionForm>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import DoctorsApi from "../api/doctors";
import type { SimpleDoctor } from "../types/doctors";
import InspectionForm from "../components/InspectionForm.vue";

const doctors = ref<SimpleDoctor[]>([]);

onMounted(async () => {
  try {
    doctors.value = await DoctorsApi.getAll();
  } catch (error) {
    console.error("Failed to load doctors:", error);
  }
});
</script>
