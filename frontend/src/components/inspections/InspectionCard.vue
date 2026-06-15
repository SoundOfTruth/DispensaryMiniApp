<template>
  <RouterLink
    :to="{
      name: 'inspections.detail',
      params: { inspectionId: props.inspection.id },
    }"
    class="inspection-card"
  >
    <div class="content">
      <div class="meta-row">
        <span class="badge">Обследование</span>
      </div>
      <div class="title">{{ props.inspection.title }}</div>
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
  color: inherit;
}

.inspection-card {
  background: var(--bg-secondary);
  min-height: 110px;
  box-sizing: border-box;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
  @media (max-width: 600px) {
    flex-direction: column;
    align-items: stretch;
    padding: 16px;
  }

  &:hover {
    border-color: #3b82f6;
    box-shadow: 0 16px 36px rgba(59, 130, 246, 0.14);
    transform: translateY(2px);
  }

  .content {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .meta-row {
    display: flex;
    align-items: center;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 8px;
    background: rgba(59, 130, 246, 0.12);
    color: #1d4ed8;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.02em;
  }

  .title {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.4;
    color: var(--text-primary);
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    white-space: normal;
  }
}
</style>
