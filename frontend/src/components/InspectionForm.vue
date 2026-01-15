<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit">
      <div class="group">
        <label for="title">Заголовок</label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          class="input-data"
          placeholder="Введите заголовок"
          required
        />
      </div>

      <div class="group">
        <label for="description">Описание</label>
        <textarea
          id="description"
          v-model="formData.description"
          class="input-data"
          rows="4"
          placeholder="Введите описание"
        ></textarea>
      </div>

      <div class="group">
        <label for="preparation">Подготовка *</label>
        <textarea
          id="preparation"
          v-model="formData.preparation"
          class="input-data"
          rows="3"
          placeholder="Опишите подготовку"
          required
        ></textarea>
      </div>

      <div class="group">
        <label>Врачи</label>

        <div class="doctor-search">
          <input
            v-model="doctorSearch"
            type="text"
            class="input-data"
            placeholder="Поиск врачей..."
          />
        </div>

        <div class="doctors-selection">
          <div
            v-for="doctor in filteredDoctors"
            :key="doctor.id"
            class="doctor-item"
            :class="{ selected: isDoctorSelected(doctor.id) }"
            @click="toggleDoctor(doctor)"
          >
            <div class="doctor-info">
              <strong>{{ doctor.fullname }}</strong>
              <div v-if="doctor.speciality" class="speciality">
                {{ doctor.speciality }}
              </div>
              <div v-if="doctor.qualification" class="qualification">
                {{ doctor.qualification }}
              </div>
              <div class="department">
                {{ doctor.department }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedDoctors.length > 0" class="selected-doctors">
          <h4>Выбранные врачи:</h4>
          <div class="selected-list">
            <div
              v-for="doctor in selectedDoctors"
              :key="doctor.id"
              class="selected-doctor"
            >
              <span>{{ doctor.fullname }}</span>
              <button
                type="button"
                class="remove-btn"
                @click="removeDoctor(doctor.id)"
              >
                ×
              </button>
            </div>
          </div>
        </div>

        <div
          v-if="filteredDoctors.length === 0 && doctorSearch"
          class="no-doctors"
        >
          Врачи не найдены
        </div>
        <div v-if="doctorsList.length === 0" class="no-doctors">
          Список врачей пуст
        </div>
      </div>

      <!-- Кнопки формы -->
      <div class="form-actions">
        <button type="submit" class="btn save">Сохранить</button>
        <button type="button" class="btn cancel" @click="handleCancel">
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";

import type { SimpleDoctor } from "../types/doctors";
import type { CreateInspection } from "../types/inspections";
import InspectionsApi from "../api/inspections";

interface Props {
  availableDoctors?: SimpleDoctor[];
}

const props = withDefaults(defineProps<Props>(), {
  availableDoctors: () => [],
});

const formData = ref({
  title: "",
  description: "",
  preparation: "",
  doctors: [] as SimpleDoctor[],
});

const doctorSearch = ref("");
const selectedDoctors = ref<SimpleDoctor[]>(formData.value.doctors);
const doctorsList = ref<SimpleDoctor[]>(props.availableDoctors);

const filteredDoctors = computed(() => {
  const searchTerm = doctorSearch.value.toLowerCase().trim();

  if (!searchTerm) {
    return doctorsList.value.filter(
      (doctor) =>
        !selectedDoctors.value.some((selected) => selected.id === doctor.id)
    );
  }

  return doctorsList.value.filter((doctor) => {
    const matchesSearch =
      doctor.fullname.toLowerCase().includes(searchTerm) ||
      (doctor.speciality?.toLowerCase() || "").includes(searchTerm) ||
      (doctor.qualification?.toLowerCase() || "").includes(searchTerm) ||
      doctor.department.toLowerCase().includes(searchTerm);

    const notSelected = !selectedDoctors.value.some(
      (selected) => selected.id === doctor.id
    );

    return matchesSearch && notSelected;
  });
});

const isDoctorSelected = (doctorId: number) => {
  return selectedDoctors.value.some((doctor) => doctor.id === doctorId);
};

const toggleDoctor = (doctor: SimpleDoctor) => {
  const index = selectedDoctors.value.findIndex((d) => d.id === doctor.id);
  if (index === -1) {
    selectedDoctors.value.push(doctor);
  } else {
    selectedDoctors.value.splice(index, 1);
  }
};

const removeDoctor = (doctorId: number) => {
  selectedDoctors.value = selectedDoctors.value.filter(
    (doctor) => doctor.id !== doctorId
  );
};

watch(
  () => props.availableDoctors,
  (newDoctors) => {
    if (newDoctors && newDoctors.length > 0) {
      doctorsList.value = newDoctors;
    }
  },
  { immediate: true }
);

const handleSubmit = async () => {
  const payload: CreateInspection = {
    title: formData.value.title,
    description: formData.value.description,
    preparation: formData.value.preparation,
    doctors: selectedDoctors.value.map((doctor) => ({
      id: doctor.id,
    })),
  };

  if (!payload.title || !payload.preparation || payload.doctors.length < 1) {
    alert("Пожалуйста, заполните обязательные поля (Заголовок и Описание)");
    return;
  }
  console.log(payload);
  const inspection = await InspectionsApi.create(payload);
  console.log(inspection);
};

const handleCancel = () => {
  console.log("cance;");
};
</script>

<style scoped lang="scss">
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

textarea.input-data {
  resize: vertical;
  min-height: 100px;
}

.doctor-search {
  margin-bottom: 16px;
}

.doctors-selection {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 16px;
  .doctor-item {
    padding: 12px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
    .selected {
      background-color: #e7f3ff;
      border-left: 3px solid #007bff;
    }
    &:hover {
      background-color: #f8f9fa;
    }
  }
}

.doctor-info {
  font-size: 14px;
  .speciality {
    color: #b1b2b4;
    font-size: 13px;
    margin-top: 2px;
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

.selected-list {
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
