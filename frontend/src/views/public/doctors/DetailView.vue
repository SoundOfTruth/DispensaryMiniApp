<template>
  <div class="doctor-page">
    <div class="err-handler" v-for="err in errors" v-if="!doctor || doctor.id !== doctorId">
      {{ err.message }}
    </div>
    <div class="doctor-container" v-else>
      <div class="doctor-header">
        <div class="doctor-img-container">
          <img
            :src="
              !doctor.photo || !doctor.photo.includes('http') ? '/static/doctor.png' : doctor.photo
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
        <div class="expirience" v-if="doctor?.experience.length !== 0">
          <span>Опыт работы: </span>
          <span>{{ doctor?.experience }}</span>
        </div>
        <div v-if="doctor?.qualification">
          <div class="sub-title">Квалификация</div>
          <span>{{ doctor?.qualification }}</span>
        </div>
        <div v-if="doctor?.education?.length">
          <div class="sub-title">Образование</div>
          <div class="education-list">
            <div v-for="education in doctor?.education">
              <div class="education-title">{{ education }}</div>
            </div>
          </div>
        </div>
        <div v-if="doctor?.extra_education?.length">
          <div class="sub-title">Доп. образование</div>
          <div class="education-list">
            <div v-for="education in doctor?.extra_education">
              <div class="education-title">{{ education }}</div>
            </div>
          </div>
        </div>
        <div class="sub-title" v-if="doctor?.inspections?.length > 0">Проводит обследования:</div>
        <div v-for="inspection in doctor?.inspections">
          <RouterLink :to="`/inspections/${inspection.id}`">{{ `${inspection.title}` }}</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

import { useDoctorStore } from '@/stores/doctors';
import { useErrorStore } from '@/stores/errors';

const route = useRoute();
const doctorId: number = Number(route.params.doctorId);

const errorStore = useErrorStore();
const doctorStore = useDoctorStore();
const doctor = computed(() => doctorStore.doctor);
const errors = computed(() => errorStore.errors);

const infoExists = computed(() =>
  Boolean(
    doctor.value?.experience ||
    doctor.value?.qualification ||
    doctor.value?.education.length != 0 ||
    doctor.value?.extra_education.length != 0 ||
    doctor.value.inspections.length != 0
  )
);

onMounted(async () => {
  await doctorStore.loadById(doctorId);
});
</script>

<style scoped lang="scss">
$primary: #0d9ce3;
$text-secondary: #6c757d;
.doctor-page {
  overflow-y: auto;
  padding-inline: 15px;
  padding-bottom: 15px;
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
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-top: 20px;
  @media (min-width: 600px) {
    padding: 8px;
    gap: 26px;
    flex-direction: row;
  }
  .doctor-img-container {
    display: grid;
    place-content: center;
    @media (min-width: 600px) {
      width: 200px;
      padding: 8px;
    }
    .doctor-img {
      width: 100%;
      height: auto;
      max-width: 500px;
      border-radius: 8px;
      @media (min-width: 600px) {
        max-width: 180px;
      }
    }
  }
}

.doctor-header-info {
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  @media (min-width: 600px) {
    padding-top: 20px;
  }
  .doctor-fullname {
    font-size: 1.6rem;
    font-weight: 600;
    line-height: 1.1;
    display: flex;
    flex-direction: column;
    gap: 2px;
    @media (min-width: 600px) {
      gap: 7px;
    }
  }
  .doctor-speciality {
    font-size: 1.15rem;
    font-weight: 500;
    color: $primary;
  }
  .doctor-department {
    font-size: 0.95rem;
    font-weight: 500;
    color: $text-secondary;
  }
}

.doctor-extra-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-top: 20px;

  .title {
    font-size: 1.25rem;
    font-weight: 500;
    padding-bottom: 8px;
  }

  .sub-title {
    padding-top: 8px;
    padding-bottom: 4px;
    font-size: 0.85rem;
    font-weight: 600;
    color: $text-secondary;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .education-list {
    display: flex;
    flex-direction: column;
    gap: 2px;

    .education-title {
      font-size: 0.95rem;
      font-weight: 400;
      padding: 6px 0;
      position: relative;
    }
  }

  .expirience {
    font-size: 1.05rem;
  }

  a {
    color: $primary;
    text-decoration: none;
    padding: 0;
    display: inline-block;
  }
}
</style>
