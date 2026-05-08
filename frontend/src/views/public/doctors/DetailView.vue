<template>
  <div class="doctor-page">
    <div class="err-handler" v-for="err in doctorStore.errors" v-if="!doctor">
      {{ err.message }}
    </div>
    <div class="doctor-container" v-else>
      <div class="description">
        <div class="doctor-img-container">
          <img
            src="/src/images/avatar.png"
            class="doctor-img"
            v-if="!doctor.photo"
          />
          <img :src="doctor.photo" class="doctor-img" v-else />
        </div>
        <div class="fullname">
          <div>{{ doctor?.lastname }}</div>
          <div>{{ doctor?.firstname }} {{ doctor?.middlename }}</div>
          <div class="speciality">
            {{ doctor?.speciality.name }}
          </div>
        </div>
      </div>
      <div class="information">
        <div class="title">Информация</div>
        <div class="expirience" v-if="doctor?.experience">
          <span>Опыт работы: </span>
          <span>{{ doctor?.experience }}</span>
        </div>
        <div>
          <div class="title">Отделение</div>
          <span>{{ doctor?.department.name }}</span>
        </div>
        <div v-if="doctor?.qualification">
          <div class="title">Квалификация</div>
          <span>{{ doctor?.qualification }}</span>
        </div>
        <div v-if="doctor?.education?.length">
          <div class="title">Образование</div>
          <div class="education">
            <div v-for="education in doctor?.extra_education">
              {{ education }}
            </div>
          </div>
        </div>
        <div v-if="doctor?.extra_education?.length">
          <div class="title">Доп. образование</div>
          <div class="education">
            <div v-for="education in doctor?.extra_education">
              {{ education }}
            </div>
          </div>
        </div>
        <div class="title" v-if="doctor?.inspections?.length > 0">
          Проводит обследования:
        </div>
        <div v-for="inspection in doctor?.inspections">
          <RouterLink :to="`/inspections/${inspection.id}`">{{
            `${inspection.title}`
          }}</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";

import { useDoctorStore } from "@/stores/doctors";

const route = useRoute();
const doctorStore = useDoctorStore();
const doctor = computed(() => doctorStore.doctor);

onMounted(async () => {
  const doctorId: number = Number(route.params.doctorId);
  await doctorStore.loadById(doctorId);
});
</script>

<style scoped lang="scss">
.doctor-page {
  overflow-y: auto;
  padding: 15px;
}
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 110%;
}
.doctor-container {
  display: flex;
  flex-direction: column;
}
.description {
  display: flex;
  gap: 50px;
  flex-direction: column;
  @media (min-width: 520px) {
    flex-direction: row;
  }
}

.doctor-img-container {
  display: grid;
  place-content: center;
  padding-bottom: 18px;
  @media (min-width: 520px) {
    width: 200px;
  }
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
