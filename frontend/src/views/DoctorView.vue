<template>
  <div>
    <div class="doctor-img-container">
      <img src="/src/images/avatar.png" class="doctor-img" />
    </div>
    <div class="fullname">
      <div>{{ doctor?.lastname }}</div>
      <div>{{ doctor?.firstname }} {{ doctor?.middlename }}</div>
    </div>
    <div class="information">
      <div class="speciality" v-html="doctor?.speciality"></div>
      <div class="expirience" v-if="doctor?.experience">
        <span>Опыт работы: </span>
        <span>{{ doctor?.experience }}</span>
      </div>
      <div v-if="doctor?.qualification">
        <div class="title">Квалификация</div>
        <span>{{ doctor?.qualification }}</span>
      </div>
      <div v-if="doctor?.education.length">
        <div class="title">Образование</div>
        <div class="education">
          <div v-for="education in doctor?.extra_education" class="text">
            {{ education }}
          </div>
        </div>
      </div>
      <div v-if="doctor?.extra_education.length">
        <div class="title">Доп. образование</div>
        <div class="education">
          <div v-for="education in doctor?.extra_education">
            {{ education }}
          </div>
        </div>
      </div>
      <div class="title">Проводимые иследования:</div>
      <div v-for="inspection in doctor?.inspections">
        <RouterLink :to="`/inspections/${inspection.id}`">{{
          `${inspection.title}`
        }}</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import DoctorsApi from "../api/doctors";
import type { Doctor } from "../types/doctors";

const route = useRoute();
const doctor = ref<Doctor | null>(null);
onMounted(async () => {
  const doctorId: number = Number(route.params.doctorId);
  doctor.value = await DoctorsApi.getDoctor(doctorId);
});
</script>

<style scoped lang="scss">
.doctor-img-container {
  display: grid;
  place-content: center;
  padding-bottom: 18px;
}
.doctor-img {
  width: 100%;
  height: auto;
  max-width: 500px;
  border-radius: 8px;
}
.title {
  font-size: 110%;
  color: #b1b2b4;
  line-height: 1;
  padding-bottom: 4px;
}
.information {
  display: flex;
  gap: 7px;
  flex-direction: column;
}
.education {
  display: flex;
  flex-direction: column;
  font-size: 90%;
  gap: 3px;
}
.fullname {
  font-size: 180%;
  font-weight: 500;
  line-height: 1;
}
.speciality {
  padding-top: 5px;
  font-size: 135%;
  color: #0d9ce3;
}
.expirience {
  font-size: 115%;
}
</style>
