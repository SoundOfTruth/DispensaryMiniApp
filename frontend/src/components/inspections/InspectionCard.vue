<template>
  <RouterLink
    :to="{
      name: 'inspections.detail',
      params: { inspectionId: inspection.id },
    }"
  >
    <div class="research-card">
      <div class="info">
        <div class="title">{{ props.inspection.title }}</div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import type { SimpleInspection } from "@/types/inspections";

const props = defineProps<{ inspection: SimpleInspection }>();
</script>

<style scoped lang="scss">
a {
  text-decoration: none;
  color: black;
}
.research-card {
  background: white;
  display: flex;
  border-radius: 16px;
  border: 1px solid transparent;
  .info {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 14px;
    .title {
      font-size: 110%;
      font-weight: 500;
    }
  }
}
</style>
