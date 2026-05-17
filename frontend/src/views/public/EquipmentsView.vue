<template>
  <div class="equipments">
    <div class="err-handler" v-for="err in errors">
      {{ err.message }}
    </div>
    <div v-for="type in types">
      <div class="equipment-type">{{ type.name }}</div>
      <div class="equipments-list">
        <EquipmentCard
          :equipment="equipment"
          v-for="equipment in type.equipments"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import EquipmentCard from "@/components/equipments/EquipmentCard.vue";
import { computed, onMounted } from "vue";

import { useEquipmentTypeStore } from "@/stores/equipmentTypes";
import { useErrorStore } from "@/stores/errors";

const typeStore = useEquipmentTypeStore();
const errorStore = useErrorStore();

const types = computed(() => typeStore.detailTypes);
const errors = computed(() => errorStore.errors);

onMounted(async () => {
  await typeStore.loadDetailList();
  if (errors.value.length === 0 && types.value.length === 0) {
    errorStore.setErrorMessage("Ничего не найдено...");
  }
});
</script>

<style lang="scss" scoped>
.equipments {
  padding: 20px 15px;
}
.equipment-type {
  font-weight: 600;
  font-size: 150%;
  padding-bottom: 20px;
}
.err-handler {
  display: flex;
  justify-content: center;
  font-size: 16px;
}
.equipments-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
