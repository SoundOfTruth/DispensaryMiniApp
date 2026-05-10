<script lang="ts" setup>
import TheForm from "./TheForm.vue";
import FormActions from "./FormActions.vue";

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
      message: "Название отделения не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  return isValid;
};

const updateDepartment = async () => {
  if (departmentId.value) {
    return await departmentStore.update(departmentId.value, formData.value);
  } else {
    departmentStore.errors.push({ message: "Непредвиденная ошибка." });
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
  <TheForm :store="departmentStore" @submit="handleSubmit">
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
    <FormActions :mode="mode" @cancel="handleCancel" />
  </TheForm>
</template>

<style lang="scss" scoped>
.form-title {
  margin: 0 auto;
  padding-bottom: 15px;
}
.group {
  margin-bottom: 24px;
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
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
</style>
