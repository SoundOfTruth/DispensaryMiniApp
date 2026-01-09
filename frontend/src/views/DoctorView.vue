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
      <div class="expirience">
        <span>Опыт работы: </span>
        <span>{{ doctor?.experience }}</span>
      </div>
      <div class="title">Образование</div>
      <div class="education" v-for="education in doctor?.education">
        {{ education }}
      </div>
      <div class="title">Доп. образование</div>
      <div class="education" v-for="education in doctor?.extra_education">
        {{ education }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
import { getDoctorsJsonPayload } from "../types/doctors";
const doctorId = Number(route.params.doctorId) - 1;
const doctor = getDoctorsJsonPayload()[doctorId];
</script>

<style scoped>
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
}
.information {
  display: flex;
  gap: 10px;
  flex-direction: column;
}
.education {
  font-size: 90%;
}
.expirience {
  font-size: 120%;
}
.fullname {
  font-size: 180%;
  font-weight: 500;
  line-height: 1;
}
.speciality {
  padding-top: 5px;
  font-size: 130%;
  color: #0d9ce3;
}
</style>
