<template>
  <div class="inspections">
    <div class="err-handler" v-if="errCondition">
      {{ err }}
    </div>
    <div v-else>
      <div v-for="obj in equipments">
        <div>
          <div class="equipment-type">{{ obj.type }}</div>
          <div class="equipments-list">
            <EquipmentCard
              :equipment="equipment"
              v-for="equipment in obj.equipments"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import EquipmentCard from "../components/equipments/EquipmentCard.vue";
import { computed, onMounted } from "vue";

import { useEquipmentStore } from "../stores/EquipmentStore";

const equipmentStore = useEquipmentStore();
const equipments = computed(() => equipmentStore.equipmentsGroupedByType);
const err = computed(() => equipmentStore.err);
const errCondition = computed(
  () => equipments.value == undefined || equipments.value?.length == 0,
);
onMounted(async () => {
  await equipmentStore.loadEquipmentsGroupedByType();
});
</script>

<style lang="scss" scoped>
.inspections {
  padding: 0px 15px;
}
.equipment-type {
  font-weight: 500;
  font-size: 140%;
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
