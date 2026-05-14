<template>
  <div class="doctor-page">
    <div class="err-handler" v-for="err in doctorStore.errors" v-if="!doctor">
      {{ err.message }}
    </div>
    <div class="doctor-container" v-else>
      <div class="doctor-header">
        <div class="doctor-img-container">
          <img
            :src="
              !doctor.photo || !doctor.photo.includes('http')
                ? '/src/images/avatar.png'
                : doctor.photo
            "
            class="doctor-img"
          />
        </div>
        <div class="doctor-header-info">
          <div class="doctor-fullname">
            <div>{{ doctor?.lastname }}</div>
            <div>{{ doctor?.firstname }} {{ doctor?.middlename }}</div>
          </div>
          <div class="doctor-speciality">
            {{ doctor?.speciality.name }}
          </div>
          <div class="doctor-department">{{ doctor?.department.name }}</div>
        </div>
      </div>
      <div class="doctor-extra-info">
        <div class="title" v-if="infoExists">Информация</div>
        <div class="expirience" v-if="doctor?.experience">
          <span>Опыт работы: </span>
          <span>{{ doctor?.experience }}</span>
        </div>
        <div v-if="doctor?.qualification">
          <div class="sub-title">Квалификация</div>
          <span>{{ doctor?.qualification }}</span>
        </div>
        <div v-if="doctor?.education?.length">
          <div class="sub-title">Образование</div>
          <div class="education">
            <div v-for="education in doctor?.education">
              {{ education }}
            </div>
          </div>
        </div>
        <div v-if="doctor?.extra_education?.length">
          <div class="sub-title">Доп. образование</div>
          <div class="education">
            <div v-for="education in doctor?.extra_education">
              {{ education }}
            </div>
          </div>
        </div>
        <div class="sub-title" v-if="doctor?.inspections?.length > 0">
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

const infoExists = computed(() =>
  Boolean(
    doctor.value?.experience ||
    doctor.value?.qualification ||
    doctor.value?.education.length != 0 ||
    doctor.value?.extra_education.length != 0 ||
    doctor.value.inspections.length != 0,
  ),
);

onMounted(async () => {
  const doctorId: number = Number(route.params.doctorId);
  await doctorStore.loadById(doctorId);
});
</script>

<style scoped lang="scss">
.doctor-page {
  overflow-y: auto;
  padding: 15px;
  .err-handler {
    display: flex;
    justify-content: center;
    font-size: 110%;
  }
  .doctor-container {
    display: flex;
    flex-direction: column;
  }
}
.doctor-header {
  border-radius: 8px;
  padding: 20px;
  background: white;
  display: flex;
  flex-direction: column;
  @media (min-width: 720px) {
    padding: 8px;
    gap: 26px;
    flex-direction: row;
  }
  .doctor-img-container {
    display: grid;
    place-content: center;
    @media (min-width: 720px) {
      width: 200px;
      padding: 8px;
    }
    .doctor-img {
      width: 100%;
      height: auto;
      max-width: 500px;
      border-radius: 8px;
      @media (min-width: 720px) {
        max-width: 180px;
      }
    }
  }
}

.doctor-header-info {
  max-width: 400px;
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 1px;
  @media (min-width: 720px) {
    padding-top: 20px;
  }
  .doctor-fullname {
    font-size: 170%;
    font-weight: 500;
    line-height: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
    @media (min-width: 720px) {
      gap: 7px;
    }
  }
  .doctor-speciality {
    padding-top: 5px;
    font-size: 130%;
    font-weight: 400;
    color: #0d9ce3;
  }
  .doctor-department {
    padding-top: 5px;
    font-size: 120%;
  }
}

.doctor-extra-info {
  padding-top: 24px;
  padding-left: 4px;
  display: flex;
  gap: 7px;
  flex-direction: column;
  .title {
    font-size: 130%;
    font-weight: 400;
    line-height: 1;
    padding-bottom: 4px;
  }
  .sub-title {
    font-size: 110%;
    color: #b1b2b4;
    line-height: 1;
    padding-bottom: 4px;
  }
  .education {
    display: flex;
    flex-direction: column;
    font-size: 90%;
    gap: 3px;
  }
  .expirience {
    font-size: 115%;
  }
}
</style>
