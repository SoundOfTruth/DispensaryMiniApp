<script lang="ts" setup>
import TheForm from "./TheForm.vue";
import FormActions from "./FormActions.vue";
import FileInput from "./FileInput.vue";

import { onMounted, ref } from "vue";

import { useRoute, useRouter } from "vue-router";

import { useEquipmentStore } from "@/stores/equipments";
import { useEquipmentTypeStore } from "@/stores/equipmentTypes";
import type { CreateEquipment } from "@/types/equipments";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();
const equipmentStore = useEquipmentStore();
const typeStore = useEquipmentTypeStore();

const equipmentId = ref<number>();
const formData = ref<CreateEquipment>({
  name: "",
  image: "",
  type_id: 0,
});

const setImage = (url: string) => {
  formData.value.image = url;
};

const getPatchPayload = (): Partial<CreateEquipment> | null => {
  const form = formData.value;
  const payload = { ...form } as Partial<CreateEquipment>;
  const equipment = equipmentStore.equipment;
  if (!equipment) {
    equipmentStore.errors.push({
      message: "Непредвиденная ошибка",
    });
    return null;
  }
  const entries = Object.entries(form) as [
    keyof CreateEquipment,
    CreateEquipment[keyof CreateEquipment],
  ][];
  entries.forEach(([key, val]) => {
    if (equipment[key] == val) {
      payload[key] = undefined;
    }
  });
  if (JSON.stringify(payload) === "{}") {
    equipmentStore.errors.push({
      message: "Nothing to update.",
    });
    return null;
  }
  return payload;
};

const validateForm = (): boolean => {
  const form = formData.value;
  let isValid: boolean = true;
  if (form.name.length < 1) {
    equipmentStore.errors.push({
      message: "Название оборудования не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  if (form.image.length < 1) {
    equipmentStore.errors.push({
      message: "Изображение не загружено.",
    });
    isValid = false;
  }
  if (form.type_id == 0) {
    equipmentStore.errors.push({
      message: "Некорректный тип оборудования.",
    });
    isValid = false;
  }
  return isValid;
};

const updateEquipment = async () => {
  if (equipmentId.value) {
    const updatePayload = getPatchPayload();
    if (updatePayload) {
      return await equipmentStore.update(equipmentId.value, updatePayload);
    }
  } else {
    equipmentStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode === "create") {
      const created = await equipmentStore.create(formData.value);
      if (created) {
        router.go(-1);
      }
    }
    if (props.mode === "edit") {
      const updated = await updateEquipment();
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
  await typeStore.loadList();
  if (props.mode !== "create") {
    equipmentId.value = Number(route.params.id);
    await equipmentStore.loadById(equipmentId.value);
    if (equipmentStore.equipment) {
      formData.value = { ...equipmentStore.equipment };
    }
  }
});
</script>

<template>
  <TheForm :store="equipmentStore"  @submit="handleSubmit">
    <h3 class="form-title">
      {{
        mode === "detail"
          ? "Просмотр оборудования"
          : mode === "edit"
            ? "Редактирование оборудования"
            : "Добавить оборудование"
      }}
    </h3>

    <div class="group" v-if="equipmentId">
      <label>Id</label>
      <input v-model="equipmentId" class="field" disabled="true" />
    </div>

    <div class="group">
      <label for="name">Название *</label>
      <input
        id="name"
        v-model="formData.name"
        type="text"
        class="field"
        placeholder="Введите название оборудования"
        required
        :disabled="mode === 'detail'"
      />
    </div>

    <div class="group">
      <label for="name">Изображение *</label>
      <FileInput
        @on-select="setImage"
        :hidden="mode === 'detail'"
        :preview-url="formData.image"
      />
    </div>

    <div class="group">
      <label for="name">Тип оборудования *</label>
      <select
        class="field"
        v-model="formData.type_id"
        :disabled="mode === 'detail' || typeStore.types.length == 0"
      >
        <option
          :value="type.id"
          v-for="type in typeStore.types"
          v-if="typeStore.types.length > 0"
        >
          {{ type.name }}
        </option>
        <option :value="0" disabled v-else>
          Нет доступных типов, вы не можете сохранять данные, пока не создадите
          тип
        </option>
      </select>
    </div>

    <FormActions :mode="mode" @cancel="handleCancel" />
  </TheForm>
</template>

<style lang="scss" scoped>
.upload-image {
  background: transparent;
}
.preview-img {
  padding-top: 15px;
  img {
    max-width: 300px;
  }
}
.form-title {
  margin: 0 auto;
  padding-bottom: 15px;
}
.group {
  margin-bottom: 20px;
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
