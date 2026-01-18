<template>
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

      <div class="form-actions">
        <button type="submit" class="btn save">Сохранить</button>
        <button type="button" class="btn cancel" @click="handleCancel()">
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import DoctorsApi from "../api/doctors";
import type { CreateDoctor } from "../types/doctors";
import type { Department } from "../types/departments";
import type { Speciality } from "../types/specialities";

const props = defineProps<{
  departments: Department[];
  specialities: Speciality[];
}>();
const emits = defineEmits(["cancel"]);

const formData = ref({
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
</style>
