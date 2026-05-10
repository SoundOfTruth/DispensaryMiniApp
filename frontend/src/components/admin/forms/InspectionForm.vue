<script setup lang="ts">
import TheForm from "./TheForm.vue";

import FormSearchField from "./FormSearchField.vue";
import FormActions from "./FormActions.vue";

import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

import { useInspectionStore } from "@/stores/inspections";
import { useDoctorStore } from "@/stores/doctors";

import type { SimpleDoctor } from "@/types/doctors";
import type { CreateInspection } from "@/types/inspections";
const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();
const emits = defineEmits(["cancel"]);

const route = useRoute();
const router = useRouter();
const inspectionId = ref<number>();
const inspectionStore = useInspectionStore();
const doctorStore = useDoctorStore();

const doctors = computed(() => doctorStore.doctors);

interface FormData {
  title: string;
  description: string;
  preparation: string;
  doctors: SimpleDoctor[];
}

const formData = ref<FormData>({
  title: "",
  description: "",
  preparation: "",
  doctors: [],
});

const doctorSearch = computed(() => route.query.search as string | undefined);

const availableDoctors = computed(() => {
  return doctors.value.filter((doctor) => {
    return !formData.value.doctors.some(
      (selected) => selected.id === doctor.id,
    );
  });
});

const selectDoctor = (doctor: SimpleDoctor) => {
  const index = formData.value.doctors.findIndex((d) => d.id === doctor.id);
  if (index === -1) {
    formData.value.doctors.push(doctor);
  } else {
    formData.value.doctors.splice(index, 1);
  }
};

const removeDoctor = (doctorId: number) => {
  formData.value.doctors = formData.value.doctors.filter(
    (doctor) => doctor.id !== doctorId,
  );
};

const validateForm = (): boolean => {
  const form = formData.value;
  let isValid = true;
  if (form.title.length < 1) {
    inspectionStore.errors.push({
      message: "Заголовок не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  if (form.preparation.length < 1) {
    inspectionStore.errors.push({
      message: "Подготовка не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  return isValid;
};

const getPatchPayload = (): Partial<CreateInspection> | null => {
  const inspection = inspectionStore.inspection;
  if (!inspection) {
    inspectionStore.errors.push({
      message: "Непредвиденная ошибка.",
    });
    return null;
  }

  const { doctors, ...form } = formData.value;
  const entries = Object.entries(form) as [
    keyof typeof form,
    (typeof form)[keyof typeof form],
  ][];
  let doctorsIsEqual = doctors.length === inspection.doctors.length;
  if (doctorsIsEqual) {
    doctorsIsEqual = doctors.every((formDoctor) =>
      inspection.doctors.find((doctor) => {
        return doctor.id == formDoctor.id;
      }),
    );
  }
  const payload: Partial<CreateInspection> = {
    doctors: doctorsIsEqual ? undefined : doctors,
  };

  entries.forEach(([key, val]) => {
    if (inspection[key] === val) {
      payload[key] = undefined;
    }
  });

  if (JSON.stringify(payload) === "{}") {
    inspectionStore.errors.push({
      message: "Nothing to update.",
    });
    return null;
  }
  return payload;
};

const createInspection = async () => {
  const payload: CreateInspection = {
    title: formData.value.title,
    description: formData.value.description,
    preparation: formData.value.preparation,
    doctors: formData.value.doctors.map((doctor) => ({
      id: doctor.id,
    })),
  };
  return await inspectionStore.create(payload);
};

const updateInspection = async () => {
  if (inspectionId.value) {
    const updatePayload = getPatchPayload();
    if (updatePayload) {
      return await inspectionStore.update(inspectionId.value, updatePayload);
    }
  } else {
    inspectionStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode == "create") {
      const created = await createInspection();
      if (created) {
        router.go(-1);
      }
    } else if (props.mode == "edit") {
      const updated = await updateInspection();
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
  if (props.mode != "detail") {
    await doctorStore.loadList();
  }
  if (props.mode !== "create") {
    inspectionId.value = Number(route.params.id);
    await inspectionStore.loadById(inspectionId.value);
    if (inspectionStore.inspection) {
      const { doctors, ...data } = inspectionStore.inspection;
      formData.value = { ...data, doctors: [...doctors] };
    }
  }
});

watch(
  () => [doctorSearch],
  async () => {
    await doctorStore.loadList();
  },
  { deep: true },
);
</script>

<template>
  <TheForm :store="inspectionStore" @submit="handleSubmit">
    <h3 class="form-title">
      {{
        mode === "detail"
          ? "Просмотр данных обследования"
          : mode === "edit"
            ? "Редактирование данных обследования"
            : "Добавить обследования"
      }}
    </h3>

    <div class="group">
      <label for="title">Заголовок *</label>
      <input
        class="field"
        id="title"
        v-model="formData.title"
        placeholder="Введите заголовок"
        required
        :disabled="mode === 'detail'"
        @keydown.enter.prevent
      />
    </div>

    <div class="group">
      <label for="description">Описание</label>
      <textarea
        class="field"
        id="description"
        v-model="formData.description"
        rows="4"
        placeholder="Введите описание"
        :disabled="mode === 'detail'"
      ></textarea>
    </div>

    <div class="group">
      <label for="preparation">Подготовка *</label>
      <textarea
        id="preparation"
        v-model="formData.preparation"
        class="field"
        rows="3"
        placeholder="Опишите подготовку"
        required
        :disabled="mode === 'detail'"
      ></textarea>
    </div>

    <div class="group">
      <label for="selectedDoctors">Проводят обследование</label>
      <div class="selection" id="selectedDoctors">
        <div
          v-for="doctor in formData.doctors"
          :key="doctor.id"
          class="item"
          @click="removeDoctor(doctor.id)"
        >
          <div class="item-info">
            <strong
              >{{ doctor.lastname }} {{ doctor.firstname }}
              {{ doctor.middlename }}</strong
            >
            <div v-if="doctor.speciality" class="speciality">
              Специальность: {{ doctor.speciality.name }}
            </div>
            <div v-if="doctor.qualification" class="qualification">
              Квалификация: {{ doctor.qualification }}
            </div>
            <div class="department">
              Отделение: {{ doctor.department.name }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="mode !== 'detail'">
        <label>Выбрать врача</label>

        <div class="item-search">
          <FormSearchField title="Найти врача" :pattern="doctorSearch" />
        </div>

        <div class="selection">
          <div
            v-for="doctor in availableDoctors"
            :key="doctor.id"
            class="item"
            @click="selectDoctor(doctor)"
          >
            <div class="item-info">
              <strong
                >{{ doctor.lastname }} {{ doctor.firstname }}
                {{ doctor.middlename }}</strong
              >
              <div v-if="doctor.speciality" class="speciality">
                Специальность: {{ doctor.speciality.name }}
              </div>
              <div v-if="doctor.qualification" class="qualification">
                Квалификация: {{ doctor.qualification }}
              </div>
              <div class="department">
                Отделение: {{ doctor.department.name }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="availableDoctors.length === 0">
        {{
          doctorSearch !== undefined
            ? "Ничего не найдено..."
            : "В базе нет врачей..."
        }}
      </div>
    </div>

    <FormActions :mode="mode" @cancel="handleCancel" />
  </TheForm>
</template>

<style scoped lang="scss">
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
  display: inline-block;
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

textarea.field {
  padding-left: 12px;
  resize: vertical;
  min-height: 100px;
  text-indent: 0px;
  field-sizing: content;
}

.item-search {
  margin-bottom: 16px;
}

.selection {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 16px;
  .item {
    padding: 12px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
    &:hover {
      background-color: #f8f9fa;
    }
  }
}

.item-info {
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 1px;
  font-size: 14px;
  .speciality {
    color: #b1b2b4;
  }

  .qualification {
    color: #b1b2b4;
    font-size: 12px;
    margin-top: 2px;
  }

  .department {
    color: #007bff;
    font-size: 12px;
    margin-top: 4px;
  }
}

.selected-doctors {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 6px;
  h4 {
    margin: 0 0 12px 0;
    font-size: 16px;
  }
}

.selecteds {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  width: max-content;
  gap: 8px;
  .selected-doctor {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #e7f3ff;
    padding: 7px 0;
    text-indent: 12px;
    border-radius: 8px;
    font-size: 13px;
    border: 1px solid #b3d7ff;

    .remove-btn {
      background: transparent;
      border: none;
      color: #dc3545;
      cursor: pointer;
      padding: 2px;
      margin-left: 15px;
      margin-right: 15px;
      font-size: 20px;
      line-height: 1;
      border-radius: 20%;

      transition: background-color 0.2s;
      &:hover {
        background-color: rgba(220, 53, 69, 0.1);
      }
    }
  }
}
</style>
