<template>
  <div class="form-actions" v-if="mode != 'detail'">
    <button type="submit" class="btn save">Сохранить</button>
    <button type="button" class="btn cancel" @click="emits('cancel')">
      Отмена
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ mode: "create" | "edit" | "detail" }>();
const emits = defineEmits(["cancel"]);
</script>

<style lang="scss" scoped>
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  @media (max-width: 768px) {
    flex-direction: column;
  }
  .btn {
    padding: 10px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
    @media (max-width: 768px) {
      width: 100%;
    }
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
