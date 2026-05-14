import { ref, computed } from "vue";
import { defineStore } from "pinia";

import type { ApiError } from "@/utils/api";

export const useErrorsStore = defineStore("errorsStore", () => {
  const _errors = ref<ApiError[]>([]);
  const errors = computed(() => {
    const copy = { ..._errors.value };
    _errors.value = [];
    return copy;
  });
  const addErrorMessage = (message: string) => {
    _errors.value.push({ message: message });
  };
  const setErrorMessage = (message: string) => {
    _errors.value = [{ message: message }];
  };
  const addError = (error: ApiError) => {
    _errors.value.push(error);
  };
  const setError = (error: ApiError) => {
    _errors.value = [error];
  };
  return { errors, addErrorMessage, setErrorMessage, addError, setError };
});
