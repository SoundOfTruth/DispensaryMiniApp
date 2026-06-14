<template>
  <RouterLink
    :to="{
      name: 'inspections.detail',
      params: { inspectionId: inspection.id },
    }"
  >
    <div class="inspection-card">
      <div class="info">
        <div class="title">{{ props.inspection.title }}</div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import type { SimpleInspection } from '@/types/inspections';

const props = defineProps<{ inspection: SimpleInspection }>();
</script>

<style scoped lang="scss">
a {
  text-decoration: none;
  color: black;
}
.inspection-card {
  background: white;
  display: flex;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  &:hover {
    border-color: #3b82f6;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
    transform: translateY(2px);
  }
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
