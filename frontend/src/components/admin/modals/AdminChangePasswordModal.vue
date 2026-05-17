<template>
  <CenterModal :open="open" @close="emits('close')">
    <div class="modal-header">
      <h3>Сменить пароль</h3>
    </div>

    <form @submit.prevent="onSubmit" class="password-form">
      <div class="form-group">
        <label>Текущий пароль</label>
        <input
          type="password"
          v-model="formData.currentPassword"
          placeholder="Введите текущий пароль"
          required
        />
      </div>

      <div class="form-group">
        <label>Новый пароль</label>
        <input
          type="password"
          v-model="formData.newPassword"
          placeholder="Введите новый пароль"
          required
        />
      </div>

      <div class="form-group">
        <span v-if="errorMessage" class="error-message">{{
          errorMessage
        }}</span>
      </div>

      <div class="actions">
        <button type="submit" class="btn-submit">Сохранить</button>
        <button type="button" class="btn-cancel" @click="emits('close')">
          Отмена
        </button>
      </div>
    </form>
  </CenterModal>
</template>

<script setup lang="ts">
import { ref } from "vue";
import CenterModal from "../../CenterModal.vue";
import { useUserStore } from "@/stores/users";
import { AxiosError } from "axios";

const props = defineProps<{ open: boolean }>();
const emits = defineEmits(["close"]);

const formData = ref<{ currentPassword: string; newPassword: string }>({
  currentPassword: "",
  newPassword: "",
});
const errorMessage = ref("");

const userStore = useUserStore();

const onSubmit = async () => {
  errorMessage.value = "";
  const form = formData.value;
  if (form.newPassword.length < 8) {
    errorMessage.value = "Пароль должен состоять минимум из 8 символо.";
    return;
  }
  if (form.currentPassword == form.newPassword) {
    errorMessage.value = "Пароли не должны совпадать.";
    return;
  }
  try {
    await userStore.changePassword(form.currentPassword, form.newPassword);
    emits("close");
  } catch (error) {
    if (error instanceof AxiosError) {
      const detail = error.response?.data?.detail;
      if (typeof detail === "string") {
        errorMessage.value = detail;
      } else {
        errorMessage.value = "Непредвиденная ошибка";
      }
    }
  }
};
</script>

<style scoped>
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  h3 {
    margin: 0;
    color: #333;
    font-size: 1.25rem;
  }
}

.password-form {
  padding: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #555;
    font-size: 0.9rem;
    font-weight: 500;
  }
  input {
    box-sizing: border-box;
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: border-color 0.2s;
    &:focus {
      outline: none;
      border-color: #667eea;
    }
  }
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-submit {
  color: white;
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-cancel {
  background: #6c757d;
  &:hover {
    background: #545b62;
  }
}

.btn-submit {
  background: #007bff;
  &:hover:not(:disabled) {
    opacity: 0.9;
  }
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.error-message {
  display: block;
  margin-top: 0.5rem;
  color: #e74c3c;
  font-size: 0.8rem;
}
</style>
