<script lang="ts" setup>
import { onMounted, ref } from "vue";

import { useRoute, useRouter } from "vue-router";

import { useSpecialityStore } from "@/stores/specialties";
import type { CreateSpeciality } from "@/types/specialities";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();
const specialityStore = useSpecialityStore();

const specialityId = ref<number>();
const formData = ref<CreateSpeciality>({ name: "" });

const validateForm = (payload: CreateSpeciality): boolean => {
  let isValid: boolean = true;
  if (payload.name.length < 1) {
    specialityStore.errors.push({
      message:
        "Название специальности не может содержать менее 1 символа",
    });
    isValid = false;
  }
  return isValid;
};

const updateSpeciality = async () => {
  if (specialityId.value) {
    return await specialityStore.update(specialityId.value, formData.value);
  } else {
    specialityStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  const payload = formData.value;
  if (validateForm(payload)) {
    if (props.mode === "create") {
      const created = await specialityStore.create(formData.value);
      if (created) {
        router.go(-1);
      }
    }
    if (props.mode === "edit") {
      const updated = await updateSpeciality();
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
    specialityId.value = Number(route.params.id);
    await specialityStore.loadById(specialityId.value);
    if (specialityStore.speciality) {
      formData.value = specialityStore.speciality;
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
            ? "Просмотр специальности"
            : mode === "edit"
              ? "Редактирование данных специальности"
              : "Добавить специальность"
        }}
      </h3>

      <div class="group" v-if="specialityId">
        <label>Id</label>
        <input v-model="specialityId" class="field" disabled="true" />
      </div>

      <div class="group">
        <label for="name">Название специальности *</label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          class="field"
          placeholder="Введите название специальности"
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
