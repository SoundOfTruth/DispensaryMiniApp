<script lang="ts" setup>
import AdminErrorModal from "../modals/AdminErrorModal.vue";
import FormSearchField from "./FormSearchField.vue";
import FileInput from "./FileInput.vue";

import { onMounted, ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useDoctorStore } from "@/stores/doctors";
import { useDepartmentStore } from "@/stores/departments";
import { useSpecialityStore } from "@/stores/specialties";
import { useInspectionStore } from "@/stores/inspections";

import type { CreateDoctor, CreateDoctorForm } from "@/types/doctors";
import type { SimpleInspection } from "@/types/inspections";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();

const doctorStore = useDoctorStore();
const departmentStore = useDepartmentStore();
const specialityStore = useSpecialityStore();
const inspectionStore = useInspectionStore();

const departments = computed(() => departmentStore.departments);
const specialities = computed(() => specialityStore.specialties);
const inspections = computed(() => inspectionStore.inspections);

const inspectionSearch = computed(
  () => route.query.search as string | undefined,
);

const doctorId = ref<number>();
const formData = ref<CreateDoctorForm>({
  lastname: "",
  firstname: "",
  middlename: "",
  qualification: null,
  experience_start: null,
  speciality_id: 0,
  department_id: 0,
  photo: null,
  education: new Set<string>(),
  extra_education: new Set<string>(),
  inspections: [],
});

const educationInput = ref<string>("");
const extraEducationInput = ref<string>("");

const setPhoto = (url: string) => {
  formData.value.photo = url;
};

const addEducation = (set: Set<string>, title: string) => {
  if (set.has(title)) {
    doctorStore.errors.push({ message: `${title} уже в добавлено.` });
    return;
  }
  if (title.length > 0) {
    set.add(title);
  } else {
    doctorStore.errors.push({
      message: "Добавленное образование содержит менее 1 символа.",
    });
  }
};

const removeEducation = (set: Set<string>, title: string) => {
  set.delete(title);
};

const availableInspection = computed(() => {
  const selectedIds = formData.value.inspections.map((i) => i.id);
  return inspections.value.filter(
    (inspection) => !selectedIds.includes(inspection.id),
  );
});

const selectInspection = (inspection: SimpleInspection) => {
  const index = formData.value.inspections.findIndex(
    (d) => d.id === inspection.id,
  );
  if (index === -1) {
    formData.value.inspections.push(inspection);
  } else {
    formData.value.inspections.splice(index, 1);
  }
};

const removeInspection = (inspectionId: number) => {
  formData.value.inspections = formData.value.inspections.filter(
    (inspection) => inspection.id != inspectionId,
  );
};

const validateForm = (): boolean => {
  const payload = formData.value;
  let isValid = true;

  if (typeof payload.experience_start === "number") {
    if (payload.experience_start < 1920) {
      doctorStore.errors.push({
        message: "Начало стажа некорректно.",
      });
      isValid = false;
    }
  } else {
    formData.value.experience_start = null;
  }

  if (
    payload.lastname.length < 1 ||
    payload.firstname.length < 1 ||
    payload.middlename.length < 1
  ) {
    doctorStore.errors.push({
      message: "Фамилия/имя/очество не может содержать менее 1 символа.",
    });
    isValid = false;
  }
  if (payload.qualification && payload.qualification.length < 1) {
    doctorStore.errors.push({
      message: "Поле квалификация не может содержать менее 1 символа.",
    });
    isValid = false;
  }

  if (payload.department_id == 0) {
    doctorStore.errors.push({
      message: "Отделение некорректно.",
    });
    isValid = false;
  }
  if (payload.speciality_id == 0) {
    doctorStore.errors.push({
      message: "Специальность некорректна.",
    });
    isValid = false;
  }
  return isValid;
};

const getPatchPayload = (): Partial<CreateDoctor> | null => {
  const doctor = doctorStore.doctor;
  if (!doctor) {
    inspectionStore.errors.push({
      message: "Непредвиденная ошибка.",
    });
    return null;
  }
  const {
    speciality_id,
    department_id,
    experience_start,
    education,
    extra_education,
    inspections,
    ...form
  } = formData.value;

  let inspectionsIsEqual = inspections.length === doctor.inspections.length;
  if (inspectionsIsEqual) {
    inspectionsIsEqual = inspections.every((formDoctor) =>
      doctor.inspections.find((doctor) => {
        return doctor.id == formDoctor.id;
      }),
    );
  }

  const educationHasNoChanges = (
    set: Set<string>,
    array: string[],
  ): boolean => {
    return set.size === array.length && array.every((val) => set.has(val));
  };

  const validExperienceStart: number | null =
    typeof experience_start === "string" ? null : experience_start;
  const payload: Partial<CreateDoctor> = {
    department_id:
      doctor?.department.id === department_id ? undefined : department_id,
    speciality_id:
      doctor?.speciality.id === speciality_id ? undefined : speciality_id,
    experience_start:
      doctor?.experience_start === validExperienceStart
        ? undefined
        : validExperienceStart,
    inspections: inspectionsIsEqual
      ? undefined
      : inspections.map((inspection) => ({
          id: inspection.id,
        })),
    education: educationHasNoChanges(education, doctor.education)
      ? undefined
      : Array.from(education),
    extra_education: educationHasNoChanges(extra_education, doctor.extra_education)
      ? undefined
      : Array.from(extra_education),
  };

  const entries = Object.entries(form) as [
    keyof typeof form,
    keyof (typeof form)[keyof typeof form],
  ][];
  entries.forEach(([key, val]) => {
    if (doctor[key] === val) {
      payload[key] = undefined;
    }
  });
  if (JSON.stringify(payload) === "{}") {
    doctorStore.errors.push({
      message: "Nothing to update.",
    });
    return null;
  }
  return payload;
};

const createDoctor = async () => {
  const { inspections, education, extra_education, experience_start, ...data } =
    formData.value;
  const payload: CreateDoctor = {
    ...data,
    experience_start:
      typeof experience_start != "string" ? experience_start : null,
    education: Array.from(education),
    extra_education: Array.from(extra_education),
    inspections: inspections.map((inspection) => ({
      id: inspection.id,
    })),
  };
  return await doctorStore.create(payload);
};

const updateDoctor = async () => {
  if (doctorId.value) {
    const updatePayload = getPatchPayload();
    if (updatePayload) {
      return await doctorStore.update(doctorId.value, updatePayload);
    }
  } else {
    doctorStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode === "create") {
      const created = await createDoctor();
      if (created) {
        router.go(-1);
      }
    } else if (props.mode == "edit") {
      const updated = await updateDoctor();
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
  await departmentStore.loadList();
  await specialityStore.loadList();
  if (props.mode != "detail") {
    await inspectionStore.loadList();
  }
  if (props.mode != "create") {
    doctorId.value = Number(route.params.id);
    if (!doctorId.value) {
      doctorStore.errors.push({ message: "Непредвиденная ошибка." });
      return;
    }
    await doctorStore.loadById(doctorId.value);
    if (doctorStore.apiDoctor) {
      const {
        extra_education,
        education,
        speciality,
        department,
        experience_years,
        inspections,
        ...data
      } = doctorStore.apiDoctor;
      formData.value = {
        ...data,
        education: new Set<string>(education),
        extra_education: new Set<string>(extra_education),
        speciality_id: speciality?.id,
        department_id: department?.id,
        inspections: [...inspections],
      };
    }
  }
});

watch(
  () => [inspectionSearch],
  async () => {
    await inspectionStore.loadList();
  },
  { deep: true },
);
</script>

<template>
  <div class="form-container">
    <form @keydown.enter.prevent @submit.prevent="handleSubmit()">
      <h3 class="form-title">
        {{
          mode === "detail"
            ? "Просмотр данных врача"
            : mode === "edit"
              ? "Редактирование данных врача"
              : "Добавить врача"
        }}
      </h3>

      <div class="group" v-if="doctorId">
        <label>Id</label>
        <input v-model="doctorId" class="field" disabled="true" />
      </div>

      <div class="group">
        <label for="name">Фото</label>
        <FileInput
          @on-select="setPhoto"
          :hidden="mode === 'detail'"
          :preview-url="formData.photo"
        />
      </div>

      <div class="group">
        <label>Фамилия *</label>
        <input
          v-model="formData.lastname"
          class="field"
          placeholder="Введите фамилию"
          required
          :disabled="mode === 'detail'"
        />
      </div>

      <div class="group">
        <label>Имя *</label>
        <input
          v-model="formData.firstname"
          class="field"
          placeholder="Введите имя"
          required
          :disabled="mode === 'detail'"
        />
      </div>

      <div class="group">
        <label>Отчество *</label>
        <input
          v-model="formData.middlename"
          class="field"
          placeholder="Введите отчество"
          required
          :disabled="mode === 'detail'"
        />
      </div>

      <div class="group">
        <label>Специальность *</label>
        <select
          v-model="formData.speciality_id"
          class="field"
          :disabled="mode === 'detail' || specialities.length == 0"
        >
          <option
            :value="speciality.id"
            v-for="speciality in specialities"
            v-if="specialities.length > 0"
          >
            {{ speciality.name }}
          </option>
          <option :value="0" disabled v-else>
            Нет доступных специальностей, вы не можете сохранять данные, пока не
            создадите специальность
          </option>
        </select>
      </div>

      <div class="group">
        <label>Отделение *</label>
        <select
          v-model="formData.department_id"
          class="field"
          :disabled="mode === 'detail' || departments.length == 0"
        >
          <option
            :value="department.id"
            v-for="department in departments"
            v-if="departments.length > 0"
          >
            {{ department.name }}
          </option>
          <option :value="0" disabled v-else>
            Нет доступных отделений, вы не можете сохранять данные, пока не
            создадите отделение
          </option>
        </select>
      </div>

      <div class="group">
        <label>Год начала стажа</label>
        <input
          type="number"
          v-model="formData.experience_start"
          class="field"
          :placeholder="
            mode !== 'detail' ? 'Введите год начала рабочего стажа' : ''
          "
          :disabled="mode === 'detail'"
        />
      </div>

      <div class="group">
        <label>Квалификационная категория</label>
        <input
          v-model="formData.qualification"
          class="field"
          :placeholder="
            mode !== 'detail' ? 'Введите квалификационную категорию' : ''
          "
          :disabled="mode === 'detail'"
        />
      </div>

      <div class="group">
        <label>Образование</label>
        <div class="education-input" v-if="mode !== 'detail'">
          <input
            v-model="educationInput"
            class="field"
            placeholder="Введите образование"
          />
          <button
            type="button"
            class="add-btn"
            @click="addEducation(formData.education, educationInput)"
          >
            <span>+</span>
          </button>
        </div>
      </div>

      <div class="group" v-if="formData.education.size > 0">
        <div class="education-list">
          <div
            v-for="education in formData.education"
            :key="education"
            class="education"
          >
            <span>{{ education }}</span>
            <button
              type="button"
              class="remove-btn"
              @click="removeEducation(formData.education, education)"
              v-if="mode !== 'detail'"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      <div class="group">
        <label>Доп. Образование</label>
        <div class="education-input" v-if="mode !== 'detail'">
          <input
            id="extra_education"
            v-model="extraEducationInput"
            type="text"
            class="field"
            placeholder="Введите доп. образование"
          />
          <button
            type="button"
            class="add-btn"
            @click="addEducation(formData.extra_education, extraEducationInput)"
          >
            <span>+</span>
          </button>
        </div>
      </div>

      <div class="group" v-if="formData.extra_education.size > 0">
        <div class="education-list">
          <div
            v-for="education in formData.extra_education"
            :key="education"
            class="education"
          >
            <span>{{ education }}</span>
            <button
              type="button"
              v-if="mode !== 'detail'"
              class="remove-btn"
              @click="removeEducation(formData.extra_education, education)"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      <div class="group">
        <label>Обследования</label>
        <div class="selection">
          <button
            v-for="inspection in formData.inspections"
            :key="inspection.id"
            class="item"
            @click="removeInspection(inspection.id)"
            :disabled="mode === 'detail'"
          >
            <div class="item-info">
              <strong>{{ inspection.title }}</strong>
            </div>
          </button>
        </div>
      </div>

      <div v-if="mode !== 'detail'" class="group">
        <label>Доступные обследования</label>

        <div class="item-search">
          <FormSearchField title="Найти обследование" />
        </div>

        <div class="group">
          <div class="selection">
            <button
              v-for="inspection in availableInspection"
              :key="inspection.id"
              class="item"
              @click="selectInspection(inspection)"
            >
              <div class="item-info">
                <strong>{{ inspection.title }}</strong>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div v-if="availableInspection?.length === 0">
        {{
          inspectionSearch !== undefined
            ? "Ничего не найдено..."
            : "В базе нет врачей..."
        }}
      </div>

      <div class="form-actions" v-if="mode != 'detail'">
        <button type="submit" class="btn save">Сохранить</button>
        <button type="button" class="btn cancel" @click="handleCancel()">
          Отмена
        </button>
      </div>
    </form>
  </div>
  <Teleport to="#modals">
    <AdminErrorModal
      :errors="doctorStore.errors"
      @close="doctorStore.errors = []"
    />
  </Teleport>
</template>

<style lang="scss" scoped>
.item-search {
  margin-bottom: 16px;
}
.item-info {
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 1px;
  font-size: 14px;
}

.selection {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 16px;
  .item {
    display: flex;
    width: 100%;
    padding: 12px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
    &:hover {
      background-color: #f8f9fa;
    }
  }
}

.form-title {
  margin: 0 auto;
  padding-bottom: 15px;
}

.form-container {
  max-width: 800px;
  margin-left: 14%;
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

.education-input {
  display: flex;
  gap: 10px;
  align-items: center;
  .add-btn {
    background: #007bff;
    color: white;
    font-size: 120%;
    line-height: 1;
    padding: 0;
    width: 30px;
    height: 30px;
    text-align: center;
    margin-right: 5px;
    place-content: center;
    font-family: sans-serif;
  }
}

.education-list {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  width: max-content;
  max-width: 100%;
  gap: 8px;
  .education {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #e7f3ff;
    text-indent: 12px;
    border-radius: 8px;
    font-size: 13px;
    border: 1px solid #b3d7ff;
    span {
      padding: 7px 1.5em;
      text-indent: 0;
      word-wrap: break-word;
      overflow-wrap: break-word;
    }
  }
}

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
  font-family: sans-serif;

  transition: background-color 0.2s;
  &:hover {
    background-color: rgba(220, 53, 69, 0.1);
  }
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  .btn {
    padding: 10px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
    &.save {
      background-color: #007bff;
      color: white;
      &:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
      }
    }
    &.cancel {
      background-color: #6c757d;
      color: white;

      &:hover {
        background-color: #545b62;
        transform: translateY(-1px);
      }
    }
  }
}
</style>
