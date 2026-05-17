<template>
  <CenterModal :open="props.errors.length > 0" @close="emits('close')">
    <div class="modal-header">
      <h3>Ошибка</h3>
    </div>
    <ul>
      <li v-for="(err, i) in errors" :key="i">
        <span v-if="err.field">
          <b>{{ err.field }}</b
          >: {{ err.message }}
        </span>
        <span v-else>
          {{ err.message }}
        </span>
      </li>
    </ul>
    <div class="actions">
      <button type="button" class="btn-submit" @click="emits('close')">
        ОК
      </button>
    </div>
  </CenterModal>
</template>

<script lang="ts" setup>
import type { ApiError } from "@/stores/errors";
import CenterModal from "../../CenterModal.vue";

const props = defineProps<{
  errors: ApiError[];
}>();

const emits = defineEmits(["close"]);
</script>

<style lang="scss" scoped>
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
.actions {
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-submit {
  width: 130px;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  background: #007bff;
  &:hover:not(:disabled) {
    opacity: 0.9;
  }
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
