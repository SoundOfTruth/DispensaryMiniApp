<template>
  <CenterModal :open="props.open" @close="emits('close')">
    <div class="modal-header">
      <h3>Удалить выбранное ({{ id ? '1 элемент' : `${elementWord}` }})</h3>
    </div>
    <div class="actions">
      <button type="submit" class="btn delete" @click="processDelete()">Удалить</button>
      <button type="button" class="btn reset" @click="emits('close')">Отмена</button>
    </div>
  </CenterModal>
</template>

<script setup lang="ts">
import CenterModal from '../../CenterModal.vue';
import type { BaseStore } from '@/stores/base';
import { computed, inject, ref } from 'vue';

const props = defineProps<{
  open: boolean;
  id: number | undefined;
  selectedItems: Set<number>;
  store: BaseStore;
}>();

const data = ref<any[]>();
inject('data', data);

const emits = defineEmits(['close']);

const elementWord = computed(() => {
  const count = props.selectedItems.size;
  const lastDigit = count % 10;
  const lastTwoDigits = count % 100;

  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
    return `${count} элементов`;
  }

  if (lastDigit === 1) {
    return `${count} элемент`;
  }

  if (lastDigit >= 2 && lastDigit <= 4) {
    return `${count} элемента`;
  }

  return `${count} элементов`;
});

const processDelete = async () => {
  if (props.id) {
    await props.store.deleteById(props.id);
  } else if (props.selectedItems) {
    await props.store.deleteList(Array.from(props.selectedItems));
  }
  await props.store.loadList();
  emits('close');
};
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
    color: var(--text-primary);
    font-size: 1.25rem;
  }
}

.actions {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 20px;
  .btn {
    padding: 10px;
    width: 110px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
  }
  .delete {
    background-color: #d63939;
    color: white;
  }
  .reset {
    background-color: #6c757d;
    color: white;
  }
}
</style>
