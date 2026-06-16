<template>
  <div>
    <AdaptivePage>
      <div>
        <div v-for="type in types">
          <div class="equipment-type">{{ type.name }}</div>
          <div class="equipments-list">
            <EquipmentCard :equipment="equipment" v-for="equipment in type.equipments" />
          </div>
        </div>
      </div>
    </AdaptivePage>
    <div class="err-handler" v-for="err in errors">
      {{ err.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import EquipmentCard from '@/components/equipments/EquipmentCard.vue';
import { computed, onMounted } from 'vue';

import { useEquipmentTypeStore } from '@/stores/equipmentTypes';
import { useErrorStore } from '@/stores/errors';
import AdaptivePage from '@/components/AdaptivePage.vue';

const typeStore = useEquipmentTypeStore();
const errorStore = useErrorStore();

const types = computed(() => typeStore.detailTypes);
const errors = computed(() => errorStore.errors);

onMounted(async () => {
  await typeStore.loadDetailList();
  if (errors.value.length === 0 && types.value.length === 0) {
    errorStore.setErrorMessage('Ничего не найдено...');
  }
});
</script>

<style lang="scss" scoped>
.equipment-type {
  font-weight: 600;
  font-size: 150%;
  padding-bottom: 20px;
  padding-left: 15px;
}
.equipments-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 10px;
}
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 16px;
  font-weight: 500;
  color: #ef4444;
}
</style>
