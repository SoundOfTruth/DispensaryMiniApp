<template>
  <div>
    <h3 class="form-title">Форма создания отделения</h3>
    <div class="form-container">
      <form @submit.prevent="handleSubmit()">
        <div class="group">
          <label for="name">Название отделения</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            class="input-data"
            placeholder="Введите название отделения"
            required
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
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

import { useDepartmentStore } from "../../stores/DepartmentStore";
import type { CreateDepartment } from "../../types/departments";

const emits = defineEmits(["cancel"]);
const formData = ref<CreateDepartment>({ name: "" });

const departmentStore = useDepartmentStore();

const handleSubmit = async () => {
  await departmentStore.create(formData.value);
};
const handleCancel = () => {
  emits("cancel");
};
</script>

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

.input-data {
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
