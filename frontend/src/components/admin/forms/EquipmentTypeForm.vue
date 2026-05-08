<script lang="ts" setup>
import { onMounted, ref } from "vue";

import { useRoute, useRouter } from "vue-router";

import { useEquipmentTypeStore } from "@/stores/equipmentTypes";
import type { CreateEquipmentType } from "@/types/equipmentTypes";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();
const typeStore = useEquipmentTypeStore();

const typeId = ref<number>();
const formData = ref<CreateEquipmentType>({ name: "" });

const validateForm = (): boolean => {
  const form = formData.value;
  let isValid: boolean = true;
  if (form.name.length < 1) {
    typeStore.errors.push({
      message: "Название типа не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  return isValid;
};

const updateType = async () => {
  if (typeId.value) {
    return await typeStore.update(typeId.value, formData.value);
  } else {
    typeStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode === "create") {
      const created = await typeStore.create(formData.value);
      if (created) {
        router.go(-1);
      }
    }
    if (props.mode === "edit") {
      if (typeId.value) {
        const updated = await updateType();
        if (updated) {
          router.go(-1);
        }
      }
    }
  }
};

const handleCancel = () => {
  router.go(-1);
};

onMounted(async () => {
  if (props.mode !== "create") {
    typeId.value = Number(route.params.id);
    await typeStore.loadById(typeId.value);
    if (typeStore.type) {
      formData.value = typeStore.type;
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
            ? "Просмотр типа оборудования"
            : mode === "edit"
              ? "Редактирование тип оборудования"
              : "Добавить тип оборудования"
        }}
      </h3>

      <div class="group" v-if="typeId">
        <label>Id</label>
        <input v-model="typeId" class="field" disabled="true" />
      </div>

      <div class="group">
        <label for="name">Название типа оборудования *</label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          class="field"
          placeholder="Введите название типа оборудования"
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
