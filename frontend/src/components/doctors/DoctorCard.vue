<template>
  <div class="doctor-card" @click="openDoctor(props.doctor.id)">
    <div class="avatar-container">
      <img src="/src/images/avatar.png" class="img" />
    </div>
    <div class="info">
      <div class="fullname">{{ props.doctor.fullname }}</div>
      <div class="speciality">{{ props.doctor?.speciality }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

import type { SimpleDoctor } from "../../types/doctors";

const router = useRouter();
const props = defineProps<{ doctor: SimpleDoctor }>();

const openDoctor = (doctorId: number) => {
  router.push(`doctors/${doctorId}`);
};
</script>

<style scoped lang="scss">
.doctor-card {
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
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 14px;
    .fullname {
      font-size: 110%;
    }
    .speciality {
      font-size: 85%;
    }
  }
}
</style>
