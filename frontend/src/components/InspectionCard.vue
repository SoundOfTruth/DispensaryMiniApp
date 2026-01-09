<template>
  <div class="research-card" @click="openResearch(props.inspection.id)">
    <div class="info">
      <div class="title">{{ props.inspection.title }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import type { Inspection } from "../types/inspections";

const router = useRouter();
const props = defineProps<{ inspection: Inspection }>();

const openResearch = (inspectionId: number) => {
  router.push(`inspections/${inspectionId}`);
};
</script>

<style scoped lang="scss">
.research-card {
  background: white;
  display: flex;
  border-radius: 4px;
  border: 1px solid transparent;
  .info {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 14px;
    .title {
      font-size: 110%;
    }
  }
}
</style>
