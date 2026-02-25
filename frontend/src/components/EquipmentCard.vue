<template>
  <div class="equipment-card">
    <img :src="equipment.image" />
    <div class="name">
      {{ props.equipment.name }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { Equiment } from "../types/equipments";
const props = defineProps<{ equipment: Equiment }>();
</script>

<style lang="scss" scoped>
.equipment-card {
  display: flex;
  background: white;
  align-items: center;
  gap: 10px;
  border: 1px solid transparent;
  border-radius: 16px;
  .name {
    font-size: clamp(75%, 3.7vw, 110%);
    padding-right: 3px;
  }
  img {
    width: 292px;
    height: 270px;
    max-width: 40vw;
    max-height: 40vw;
    border-radius: 16px;
  }
}
</style>
