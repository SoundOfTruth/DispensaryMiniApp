<template>
  <div class="equipment-card">
    <div class="image-container">
      <img :src="equipment.image" :alt="equipment.name" loading="lazy" />
    </div>
    <div class="content">
      <div class="name">{{ equipment.name }}</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { Equipment } from "@/types/equipments";

defineProps<{ equipment: Equipment }>();
</script>

<style lang="scss" scoped>
.equipment-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 16px;
  transition: all 0.2s ease;

  &:hover {
    border-color: #b0b0b0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  .image-container {
    flex-shrink: 0;
    width: 80px;
    height: 80px;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;

    img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }
  }

  .content {
    flex: 1;
    min-width: 0;
  }

  .name {
    font-size: 110%;
    font-weight: 500;
    margin: 0 0 4px 0;
    line-height: 1.4;
  }

  @media (min-width: 768px) {
    gap: 24px;
    padding: 20px;

    .image-container {
      width: 100px;
      height: 100px;
    }

    .name {
      font-size: 125%;
    }
  }

  @media (min-width: 1024px) {
    .image-container {
      width: 120px;
      height: 120px;
    }
  }
}
</style>
