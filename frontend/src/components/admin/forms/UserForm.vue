<script lang="ts" setup>
import TheForm from "./TheForm.vue";
import FormActions from "./FormActions.vue";
import { onMounted, ref } from "vue";

import { useRoute, useRouter } from "vue-router";

import { useUserStore } from "@/stores/users";
import type { CreateUser } from "@/types/users";

const props = defineProps<{
  mode: "create" | "edit" | "detail";
}>();

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const userId = ref<number>();

interface FormData {
  email: string;
  lastname: string;
  firstname: string;
  middlename: string;
  password?: string;
  is_superuser: boolean;
}
const formData = ref<FormData>({
  email: "",
  lastname: "",
  firstname: "",
  middlename: "",
  password: props.mode !== "edit" ? "" : undefined,
  is_superuser: false,
});

const getPatchPayload = (): Partial<CreateUser> | null => {
  const form = formData.value;
  const payload = { ...form } as Partial<CreateUser>;
  const user = userStore.user;

  if (!user) {
    userStore.errors.push({
      message: "Непредвиденная ошибка.",
    });
    return null;
  }

  const entries = Object.entries(form) as [
    keyof FormData,
    FormData[keyof FormData],
  ][];
  entries.forEach(([key, val]) => {
    if (key != "password" && user[key] === val) {
      payload[key] = undefined;
    }
  });

  if (JSON.stringify(payload) === "{}") {
    userStore.errors.push({
      message: "Nothing to update.",
    });
    return null;
  }
  return payload;
};

const validateForm = (): boolean => {
  const form = formData.value;
  let formValid = true;
  if (
    form.lastname.length < 1 ||
    form.firstname.length < 1 ||
    form.middlename.length < 1
  ) {
    userStore.errors.push({
      message: "Фамилия/имя/очество не может содержать менее 1 символа.",
    });
    formValid = false;
  }
  if (
    (props.mode === "create" && !form.password) ||
    (form.password && form.password.length < 8)
  ) {
    userStore.errors.push({
      message: "Пароль должен состоять минимум из 8 символов.",
    });
    formValid = false;
  }
  return formValid;
};

const updateUser = async () => {
  if (userId.value) {
    const updatePayload = getPatchPayload();
    if (updatePayload) {
      return await userStore.update(userId.value, updatePayload);
    }
  } else {
    userStore.errors.push({ message: "Непредвиденная ошибка." });
  }
};

const handleSubmit = async () => {
  if (validateForm()) {
    if (props.mode === "create") {
      const created = await userStore.create(formData.value as CreateUser);
      if (created) {
        router.go(-1);
      }
    } else if (props.mode === "edit") {
      const updated = await updateUser();
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
    userId.value = Number(route.params.id);
    await userStore.loadById(userId.value);
    if (userStore.user) {
      formData.value = { ...userStore.user };
    }
  }
});
</script>

<template>
  <TheForm :store="userStore" @submit="handleSubmit">
    <h3 class="form-title">
      {{
        mode === "detail"
          ? "Просмотр пользователя"
          : mode === "edit"
            ? "Редактирование данных пользователя"
            : "Добавить пользователя"
      }}
    </h3>

    <div class="group" v-if="userId">
      <label>Id</label>
      <input v-model="userId" class="field" disabled="true" />
    </div>

    <div class="group">
      <label for="name">Фамилия *</label>
      <input
        id="name"
        v-model="formData.lastname"
        type="text"
        class="field"
        placeholder="Введите название специальности"
        required
        :disabled="mode === 'detail'"
      />
    </div>

    <div class="group">
      <label for="name">Имя *</label>
      <input
        id="name"
        v-model="formData.firstname"
        type="text"
        class="field"
        placeholder="Введите название специальности"
        required
        :disabled="mode === 'detail'"
      />
    </div>
    <div class="group">
      <label for="name">Отчество *</label>
      <input
        id="name"
        v-model="formData.middlename"
        type="text"
        class="field"
        placeholder="Введите название специальности"
        required
        :disabled="mode === 'detail'"
      />
    </div>

    <div class="group">
      <label for="name">Почта *</label>
      <input
        id="name"
        v-model="formData.email"
        type="email"
        class="field"
        placeholder="Введите почту"
        required
        :disabled="mode === 'detail'"
      />
    </div>

    <div class="group" v-if="mode !== 'detail'">
      <label for="name">Пароль *</label>
      <input
        id="name"
        v-model="formData.password"
        type="password"
        class="field"
        placeholder="Введите пароль"
        :required="mode === 'create'"
      />
    </div>

    <div class="group">
      <label for="name">Администратор? </label>
      <input type="checkbox" v-model="formData.is_superuser" />
    </div>

    <FormActions :mode="mode" @cancel="handleCancel" />
  </TheForm>
  <Teleport to="#modals">
    <AdminErrorModal
      :errors="userStore.errors"
      @close="userStore.errors = []"
    />
  </Teleport>
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
