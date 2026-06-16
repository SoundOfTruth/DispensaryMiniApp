<script setup lang="ts">
import TheForm from './TheForm.vue';

import FormActions from './FormActions.vue';

import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import { useInspectionStore } from '@/stores/inspections';
import { useDoctorStore } from '@/stores/doctors';

import type { SimpleDoctor } from '@/types/doctors';
import type { CreateInspection } from '@/types/inspections';
import { useErrorStore } from '@/stores/errors';
import LoadContainer from '@/components/LoadContainer.vue';
const props = defineProps<{
  mode: 'create' | 'edit' | 'detail';
}>();
const emits = defineEmits(['cancel']);

const route = useRoute();
const router = useRouter();
const inspectionId = ref<number>();

const errorStore = useErrorStore();
const inspectionStore = useInspectionStore();
const doctorStore = useDoctorStore();

interface FormData {
  title: string;
  description: string;
  preparation: string;
  doctors: SimpleDoctor[];
}

const formData = ref<FormData>({
  title: '',
  description: '',
  preparation: '',
  doctors: [],
});

const doctors = ref<SimpleDoctor[]>([]);

const searchDoctors = async (search: string) => {
  await doctorStore.loadList({ search: search });
  doctors.value = [...doctorStore.doctors];
};

const loadDoctors = async (filters: { page?: number; search?: string }) => {
  await doctorStore.loadList(filters);
  doctors.value.push(...doctorStore.doctors);
};

const availableDoctors = computed(() => {
  return doctors.value.filter((doctor) => {
    return !formData.value.doctors.some((selected) => selected.id === doctor.id);
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
  formData.value.doctors = formData.value.doctors.filter((doctor) => doctor.id !== doctorId);
};

const validateForm = (): boolean => {
  const form = formData.value;
  let isValid = true;
  if (form.title.length < 1) {
    errorStore.addErrorMessage('Заголовок не может содержать менее 1 символа.');
    isValid = false;
  }
  return isValid;
};

const getPatchPayload = (): Partial<CreateInspection> | null => {
  const inspection = inspectionStore.inspection;
  if (!inspection) {
    errorStore.addErrorMessage('Непредвиденная ошибка.');
    return null;
  }

  const { doctors, ...form } = formData.value;
  const entries = Object.entries(form) as [keyof typeof form, (typeof form)[keyof typeof form]][];
  let doctorsIsEqual = doctors.length === inspection.doctors.length;
  if (doctorsIsEqual) {
    doctorsIsEqual = doctors.every((formDoctor) =>
      inspection.doctors.find((doctor) => {
        return doctor.id == formDoctor.id;
      })
    );
  }
  const payload: Partial<CreateInspection> = {
    doctors: doctorsIsEqual ? undefined : doctors,
  };

  entries.forEach(([key, val]) => {
    if (inspection[key] !== val) {
      payload[key] = val;
    }
  });

  if (JSON.stringify(payload) === '{}') {
    errorStore.addErrorMessage('Nothing to update.');
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
    errorStore.addErrorMessage('Непредвиденная ошибка.');
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode == 'create') {
      const created = await createInspection();
      if (created) {
        router.go(-1);
      }
    } else if (props.mode == 'edit') {
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
  if (props.mode != 'detail') {
    await doctorStore.loadList();
    doctors.value = [...doctorStore.doctors];
  }
  if (props.mode !== 'create') {
    inspectionId.value = Number(route.params.id);
    await inspectionStore.loadById(inspectionId.value);
    if (inspectionStore.inspection) {
      const { doctors, ...data } = inspectionStore.inspection;
      formData.value = { ...data, doctors: [...doctors] };
    }
  }
});
</script>

<template>
  <TheForm @submit="handleSubmit">
    <h3 class="form-title">
      {{
        mode === 'detail'
          ? 'Просмотр данных обследования'
          : mode === 'edit'
            ? 'Редактирование данных обследования'
            : 'Добавить обследования'
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
        :disabled="mode === 'detail'"
      ></textarea>
    </div>

    <div class="group">
      <label for="selectedDoctors">Проводят обследование</label>
      <div class="selection" id="selectedDoctors">
        <button
          v-for="doctor in formData.doctors"
          :key="doctor.id"
          class="selection-item"
          :disabled="mode === 'detail'"
          @click="removeDoctor(doctor.id)"
        >
          <div class="item-info">
            <strong>{{ doctor.lastname }} {{ doctor.firstname }} {{ doctor.middlename }}</strong>
            <div v-if="doctor.speciality" class="speciality">
              Специальность: {{ doctor.speciality.name }}
            </div>
            <div v-if="doctor.qualification" class="qualification">
              Квалификация: {{ doctor.qualification }}
            </div>
            <div class="department">Отделение: {{ doctor.department.name }}</div>
          </div>
        </button>
      </div>

      <div v-if="mode !== 'detail'">
        <label>Выбрать врача</label>
        <LoadContainer
          :count="doctorStore.count"
          @load="loadDoctors"
          search-title="Найти врача"
          @search="searchDoctors"
        >
          <div
            v-for="doctor in availableDoctors"
            :key="doctor.id"
            class="selection-item"
            @click="selectDoctor(doctor)"
          >
            <div class="item-info">
              <strong>{{ doctor.lastname }} {{ doctor.firstname }} {{ doctor.middlename }}</strong>
              <div v-if="doctor.speciality" class="speciality">
                Специальность: {{ doctor.speciality.name }}
              </div>
              <div v-if="doctor.qualification" class="qualification">
                Квалификация: {{ doctor.qualification }}
              </div>
              <div class="department">Отделение: {{ doctor.department.name }}</div>
            </div>
          </div>
        </LoadContainer>
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
  box-sizing: border-box;
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
  box-sizing: border-box;
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
  box-sizing: border-box;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  background: var(--bg-secondary);
  border-radius: 8px;
  margin-bottom: 16px;
}

.selection-item {
  width: 100%;
  font-weight: 400;
  text-align: start;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
  &:hover {
    background-color: #f8f9fa;
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
