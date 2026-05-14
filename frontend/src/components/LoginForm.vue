<template>
  <form class="form-container" @submit.prevent="onSubmit()">
    <input
      required
      type="email"
      v-model="formData.email"
      placeholder="Email"
      id="name"
      class="field"
    />

    <input
      required
      type="password"
      v-model="formData.password"
      placeholder="Введите пароль"
      id="name"
      class="field"
    />
    <button class="submit-btn">Войти</button>
  </form>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";

const emits = defineEmits(["afterSubmit"]);

const authStore = useAuthStore();

const formData = ref<{ email: string; password: string }>({
  email: "",
  password: "",
});

const onSubmit = async () => {
  await authStore.login(formData.value);
  emits("afterSubmit");
};
</script>

<style lang="scss" scoped>
.form-container {
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}
.field {
  box-sizing: border-box;
  width: 100%;
  padding: 14px 0;
  text-indent: 12px;
  border: 1px solid #afb1b6;
  border-radius: 10px;
  transition: border-color 0.2s;
  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
}
.submit-btn {
  box-sizing: border-box;
  padding: 14px 0px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  background-color: #007bff;
  color: white;
  &:hover {
    background-color: #0056b3;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
  }
}
</style>
