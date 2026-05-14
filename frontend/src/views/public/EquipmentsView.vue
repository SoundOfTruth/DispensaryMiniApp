<template>
  <div class="equipments">
    <div class="err-handler" v-for="err in errors" v-if="errCondition">
      {{ err.message }}
    </div>
    <div v-for="type in types" v-else>
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

const typeStore = useEquipmentTypeStore();
const types = computed(() => typeStore.detailTypes);
const errors = computed(() => typeStore.errors);
const errCondition = computed(
  () => types.value == undefined || types.value?.length == 0,
);
onMounted(async () => {
  await typeStore.loadDetailList();
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
