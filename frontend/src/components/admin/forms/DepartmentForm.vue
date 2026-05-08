<script lang="ts" setup>
import { onMounted, ref } from "vue";

import { useRoute, useRouter } from "vue-router";

import { useDepartmentStore } from "@/stores/departments";
import type { CreateDepartment } from "@/types/departments";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();
const departmentStore = useDepartmentStore();

const departmentId = ref<number>();
const formData = ref<CreateDepartment>({ name: "" });

const validateForm = (): boolean => {
  const form = formData.value;
  let isValid: boolean = true;
  if (form.name.length < 1) {
    departmentStore.errors.push({
      message: "Название отделения должно состоять не менее, чем из 1 символа",
    });
    isValid = false;
  }
  return isValid;
};

const updateDepartment = async () => {
  if (departmentId.value) {
    return await departmentStore.update(departmentId.value, formData.value);
  } else {
    departmentStore.errors.push({ message: "Непредвиденная ошибка" });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode === "create") {
      const created = await departmentStore.create(formData.value);
      if (created) {
        router.go(-1);
      }
    }
    if (props.mode === "edit") {
      const updated = await updateDepartment();
      if (updated) {
        router.go(-1);
      }
    }
  }
};

const handleCancel = () => {
  router.go(-1);
};

onMounted(async () => {
  if (props.mode !== "create") {
    departmentId.value = Number(route.params.id);
    await departmentStore.loadById(departmentId.value);
    if (departmentStore.department) {
      formData.value = departmentStore.department;
    }
  }
});
</script>

<template>
  <div class="form-container">
    <form @keydown.enter.prevent @submit.prevent="handleSubmit()">
      <h3 class="form-title">
        {{
          mode === "detail"
            ? "Просмотр отделения"
            : mode === "edit"
              ? "Редактирование данных отделения"
              : "Добавить отделение"
        }}
      </h3>

      <div class="group" v-if="departmentId">
        <label>Id</label>
        <input v-model="departmentId" class="field" disabled="true" />
      </div>

      <div class="group">
        <label for="name">Название отделения *</label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          class="field"
          placeholder="Введите название отделения"
          required
          :disabled="mode === 'detail'"
        />
      </div>
      <div class="form-actions">
        <button type="submit" class="btn save">Сохранить</button>
        <button type="button" class="btn cancel" @click="handleCancel()">
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
.form-title {
  margin: 0 auto;
  padding-bottom: 15px;
}
.form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  .group {
    margin-bottom: 24px;
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
    }
  }
}

.field {
  width: 100%;
  padding: 10px 0;
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

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.save {
  background-color: #007bff;
  color: white;
  &:hover {
    background-color: #0056b3;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
  }
}
.cancel {
  background-color: #6c757d;
  color: white;

  &:hover {
    background-color: #545b62;
    transform: translateY(-1px);
  }
}

@media (max-width: 768px) {
  .form-container {
    padding: 15px;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
