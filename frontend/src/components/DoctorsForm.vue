<template>
  <div>
    <h3 class="form-title">Форма создания врача</h3>
    <div class="form-container">
      <form @submit.prevent="handleSubmit()">
        <div class="group">
          <label for="lastname">Фамилия *</label>
          <input
            id="lastname"
            v-model="formData.lastname"
            type="text"
            class="input-data"
            placeholder="Введите фамилию"
            required
          />
        </div>

        <div class="group">
          <label for="firstname">Имя *</label>
          <input
            id="firstname"
            v-model="formData.firstname"
            type="text"
            class="input-data"
            placeholder="Введите имя"
            required
          />
        </div>

        <div class="group">
          <label for="middlename">Отчество *</label>
          <input
            id="middlename"
            v-model="formData.middlename"
            type="text"
            class="input-data"
            placeholder="Введите отчество"
            required
          />
        </div>

        <div class="group">
          <label for="experienceStart">Год начала стажа *</label>
          <input
            id="experienceStart"
            v-model="formData.experience_start"
            type="number"
            class="input-data"
            placeholder="Введите год начала рабочего стажа"
          />
        </div>

        <div class="group">
          <label for="qualification">Квалификационная категория</label>
          <input
            id="qualification"
            v-model="formData.qualification"
            type="text"
            class="input-data"
            placeholder="Введите квалификационную категорию"
          />
        </div>

        <div class="group">
          <label for="speciality_id">Специальность</label>
          <select
            name="option"
            v-model="formData.speciality_id"
            class="input-data"
          >
            <option :value="speciality.id" v-for="speciality in specialities">
              {{ speciality.name }}
            </option>
          </select>
        </div>

        <div class="group">
          <label for="department_id">Отделение</label>
          <select
            name="option"
            v-model="formData.department_id"
            class="input-data"
          >
            <option :value="department.id" v-for="department in departments">
              {{ department.name }}
            </option>
          </select>
        </div>

        <div class="group">
          <label for="education">Образование</label>
          <div class="education-group">
            <input
              id="education"
              v-model="educationField"
              type="text"
              class="input-data"
              placeholder="Введите образование"
            />
            <button
              type="button"
              class="add"
              @click="addEducation(formData.education, educationField)"
            >
              +
            </button>
          </div>
        </div>

        <div v-if="formData.education.length > 0" class="selected-doctors">
          <div class="selected-list group">
            <div
              v-for="education in formData.education"
              :key="education.title"
              class="selected-doctor"
            >
              <span>{{ education.title }}</span>
              <button
                type="button"
                class="remove-btn"
                @click="removeEducation(education)"
              >
                ×
              </button>
            </div>
          </div>
        </div>

        <div class="group">
          <label for="extra_education">Доп. Образование</label>
          <div class="education-group">
            <input
              id="extra_education"
              v-model="extraEducationField"
              type="text"
              class="input-data"
              placeholder="Введите доп. образование"
            />
            <button
              type="button"
              class="add"
              @click="
                addEducation(formData.extra_education, extraEducationField)
              "
            >
              +
            </button>
          </div>
        </div>

        <div
          v-if="formData.extra_education.length > 0"
          class="selected-doctors"
        >
          <div class="selected-list">
            <div
              v-for="education in formData.extra_education"
              :key="education.title"
              class="selected-doctor"
            >
              <span>{{ education.title }}</span>
              <button
                type="button"
                class="remove-btn"
                @click="removeExtraEducation(education)"
              >
                ×
              </button>
            </div>
          </div>
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

import DoctorsApi from "../api/doctors";
import type { CreateDoctor, CreateEducation } from "../types/doctors";
import type { Department } from "../types/departments";
import type { Speciality } from "../types/specialities";

const props = defineProps<{
  departments: Department[];
  specialities: Speciality[];
}>();
const emits = defineEmits(["cancel"]);

const formData = ref<CreateDoctor>({
  lastname: "",
  firstname: "",
  middlename: "",
  qualification: null,
  experience_start: 0,
  department_id: 1,
  speciality_id: 1,
  education: [],
  extra_education: [],
});

const educationField = ref<string>("");
const extraEducationField = ref<string>("");

const addEducation = (array: CreateEducation[], title: string) => {
  const payload = { title: title };
  if (
    payload.title.length > 0 &&
    array.findIndex((obj) => obj.title == payload.title) == -1
  ) {
    array.push(payload);
  }
};

const removeEducation = (edication: CreateEducation) => {
  formData.value.education = formData.value.education.filter(
    (obj) => obj != edication,
  );
};

const removeExtraEducation = (edication: CreateEducation) => {
  formData.value.extra_education = formData.value.extra_education.filter(
    (obj) => obj != edication,
  );
};

const handleSubmit = async () => {
  const payload: CreateDoctor = formData.value;

  if (
    !payload.lastname ||
    !payload.firstname ||
    !payload.middlename ||
    !payload.experience_start
  ) {
    alert("Пожалуйста, заполните обязательные поля");
    return;
  }
  const doctor = await DoctorsApi.create(payload);
  console.log(doctor);
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

.education-group {
  display: flex;
  gap: 10px;
  align-items: center;
  button.add {
    background: #007bff;
    color: white;
    font-size: 120%;
    line-height: 1;
    padding: 0;
    width: 30px;
    height: 30px;
    text-align: center;
    margin-right: 5px;
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
</style>
