<template>
  <RouterLink
    :to="{
      name: 'doctors.detail',
      params: { doctorId: doctor.id },
    }"
  >
    <div class="doctor-card">
      <div class="avatar-container">
        <img
          :src="
            !doctor.photo || !doctor.photo.includes('http')
              ? 'static/doctor.png'
              : doctor.photo
          "
          class="img"
          loading="lazy"
        />
      </div>
      <div class="info">
        <div class="fullname">
          {{
            `${doctor?.lastname}  ${doctor?.firstname} ${doctor?.middlename}`
          }}
        </div>
        <div class="speciality">{{ doctor?.speciality.name }}</div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import { computed } from "vue";

import type { SimpleDoctor } from "@/types/doctors";

const props = defineProps<{ doctor: SimpleDoctor }>();
const doctor = computed(() => props.doctor);
</script>

<style scoped lang="scss">
a {
  text-decoration: none;
  color: black;
}
.doctor-card {
  min-height: 110px;
  background: white;
  display: flex;
  border-radius: 16px;
  border: 1px solid transparent;
  .avatar-container {
    display: grid;
    place-content: center;
    .img {
      width: 90px;
      border-radius: 12px;
      border: 1px solid transparent;
      padding: 8px;
    }
  }
  .info {
    padding-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-left: 14px;
    @media (max-width: 354px) {
      gap: 2px;
      padding-left: 8px;
    }
    .fullname {
      font-weight: 500;
      font-size: 110%;
      line-height: 1.2;
      @media (max-width: 354px) {
        font-size: 100%;
      }
    }
    .speciality {
      font-size: 100%;
      font-weight: 400;
      @media (max-width: 354px) {
        font-size: 70%;
      }
    }
  }
}
</style>
