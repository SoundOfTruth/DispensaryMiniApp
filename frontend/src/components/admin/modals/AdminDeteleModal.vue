<template>
  <CenterModal :open="props.open" @close="emits('close')">
    <div>
      <div class="title">Подтвердите действие</div>
    </div>
    <div class="actions">
      <button type="submit" class="btn delete" @click="processDelete()">
        Удалить
      </button>
      <button type="button" class="btn reset" @click="emits('close')">
        Отмена
      </button>
    </div>
  </CenterModal>
</template>

<script setup lang="ts">
import CenterModal from "./CenterModal.vue";
import type { BaseStore } from "@/stores/base";
import { inject, ref } from "vue";

const props = defineProps<{
  open: boolean;
  id: number | undefined;
  selectedItems: Set<number>;
  store: BaseStore;
}>();

const data = ref<any[]>();
inject("data", data);

const emits = defineEmits(["close"]);

const processDelete = async () => {
  if (props.id) {
    await props.store.deleteById(props.id);
  } else if (props.selectedItems) {
    await props.store.deleteList(Array.from(props.selectedItems));
  }
  await props.store.loadList();
  emits("close");
};
</script>

<style lang="scss" scoped>
.modal {
  z-index: 101;
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  .modal-container {
    z-index: 100;
  }
}
.modal-content {
  background: white;
  padding-inline: 20px;
  padding-bottom: 20px;
  background: white;
  border-radius: 16px;
  width: 320px;
  .title {
    padding-top: 15px;
    text-align: center;
    font-size: 110%;
    font-weight: 500;
  }
  .modal-content {
    padding: 10px;
    text-align: center;
  }
}

.actions {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding-top: 20px;
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

.modal-backdrop {
  z-index: 99;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  opacity: 0.5;
}
</style>
