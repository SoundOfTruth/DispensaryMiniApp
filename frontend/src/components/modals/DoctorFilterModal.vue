<template>
  <div class="modal" v-if="props.open">
    <div class="container">
      <div class="header">
        <h2>Фильтр</h2>
        <button @click="emit('close')" class="close"><XSvg /></button>
      </div>
      <div class="body">
        <div class="group">
          <label for="speciality_id">Специальность</label>
          <select
            id="speciality_id"
            v-model="filtersData.speciality_id"
            class="input-data"
          >
            <option :value="undefined">Выберите специальность</option>
            <option :value="speciality.id" v-for="speciality in specialities">
              {{ speciality.name }}
            </option>
          </select>
        </div>

        <div class="group">
          <label for="department_id">Отделение</label>
          <select
            id="department_id"
            v-model="filtersData.department_id"
            class="input-data"
          >
            <option :value="undefined">Выберите отделение</option>
            <option :value="department.id" v-for="department in departments">
              {{ department.name }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div class="actions">
      <button type="submit" class="btn confirm" @click="handleConfirm()">
        Применить
      </button>
      <button type="button" class="btn reset" @click="handleReset()">
        Сбросить
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import XSvg from "../svg/XSvg.vue";
import { useDepartmentStore } from "../../stores/DepartmentStore";
import { useSpecialityStore } from "../../stores/SpecialityStore";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const props = defineProps<{ open: boolean }>();
const emit = defineEmits(["close"]);

const DepartmentStore = useDepartmentStore();
const SpecialitiesStore = useSpecialityStore();
const departments = computed(() => DepartmentStore.departments);
const specialities = computed(() => SpecialitiesStore.specialities);

const filtersData = ref<{
  department_id: number | undefined;
  speciality_id: number | undefined;
}>({
  department_id: route.query.department_id
    ? Number(route.query.department_id)
    : undefined,
  speciality_id: route.query.speciality_id
    ? Number(route.query.speciality_id)
    : undefined,
});

onMounted(async () => {
  await DepartmentStore.loadDepartments();
  await SpecialitiesStore.loadSpecialities();
});

const handleReset = () => {
  filtersData.value.department_id = undefined;
  filtersData.value.speciality_id = undefined;
};
const handleConfirm = () => {
  router.push({
    path: "/doctors",
    query: { ...route.query, ...filtersData.value },
  });
  emit("close");
};
</script>

<style lang="scss" scoped>
.group {
  margin-bottom: 20px;
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
  }
  .input-data {
    width: 100%;
    padding: 12px 0;
    text-indent: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s;
    &:focus {
      outline: none;
      border-color: #007bff;
      box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
    }
  }
}

.modal {
  z-index: 99;
  position: fixed;
  padding: 20px;
  z-index: 100;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  .container {
    flex: 1;
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .close {
      padding: 0px;
      background-color: transparent;
      display: flex;
      align-items: center;
      padding-top: 5px;
    }
  }
}

.actions {
  display: flex;
  justify-content: center;
  gap: 40px;
  .btn {
    padding: 10px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
  }
  .confirm {
    background-color: #007bff;
    color: white;
  }
  .reset {
    background-color: #6c757d;
    color: white;
  }
}
</style>
