<template>
  <div class="container" v-if="isAdmin">
    <div class="card">
      <div class="hat">
        <div class="header">
          <div class="title">{{ props.title }}</div>
          <div class="actions">
            <ExportButton />
            <RouterLink
              :to="{ name: String(route.name) + '.create' }"
              class="add-btn"
            >
              {{ props.addButtonName }}</RouterLink
            >
          </div>
        </div>
        <div class="filters">
          <ActionsButton @delete="openDelete()" />
          <div class="search">
            <SearchField title="Поиск" />
          </div>
        </div>
      </div>
    </div>
    <div class="content">
      <AdminTable
        :columns="props.columns"
        :data="props.data"
        :store="store"
        :is-all-selected="isAllSelected"
        :selected-items="selectedItems"
        @select-all="selectAll"
        @select-one="selectOne"
        @open-delete="openDelete"
      />
    </div>
  </div>
  <Teleport to="#modals" v-if="isAdmin">
    <AdminDeteleModal
      :open="deleteOpen"
      :id="deleteId"
      :selected-items="selectedItems"
      :store="props.store"
      @close="closeDelete"
    />
    <AdminErrorModal :errors="store.errors" @close="store.errors = []" />
  </Teleport>
</template>

<script lang="ts" setup>
import ActionsButton from "./buttons/ActionsButton.vue";
import AdminDeteleModal from "./modals/AdminDeteleModal.vue";
import AdminErrorModal from "./modals/AdminErrorModal.vue";
import AdminTable from "./AdminTable.vue";
import SearchField from "../SearchField.vue";
import ExportButton from "./buttons/ExportButton.vue";

import type { BaseStore } from "../../stores/base";

import { onMounted, watch, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores/users";

const userStore = useUserStore();
const isAdmin = computed(() => userStore.isAdmin);

const deleteId = ref<number | undefined>(undefined);
const deleteOpen = ref<boolean>(false);

const openDelete = (id?: number) => {
  deleteId.value = id;
  if (!deleteId.value && selectedItems.value.size === 0) {
    props.store.errors.push({ message: "Ничего не выбрано." });
  } else {
    deleteOpen.value = true;
  }
};

const closeDelete = () => {
  isAllSelected.value = false;
  selectedItems.value.clear();
  deleteId.value = undefined;
  deleteOpen.value = false;
};

interface Columns {
  key: string;
  text: string;
}

interface inputData {
  title: string;
  addButtonName: string;
  columns: Columns[];
  data: any[] | undefined;
  store: BaseStore;
}

const route = useRoute();

const props = defineProps<inputData>();

const isAllSelected = ref<boolean>(false);
const selectedItems = ref<Set<number>>(new Set());

const selectAll = () => {
  if (!isAllSelected.value) {
    props.data?.forEach((val) => {
      selectedItems.value.add(val.id);
    });
    isAllSelected.value = true;
  } else {
    selectedItems.value.clear();
    isAllSelected.value = false;
  }
};

const selectOne = (id: number) => {
  if (!selectedItems.value.has(id)) {
    selectedItems.value.add(id);
  } else {
    selectedItems.value.delete(id);
  }
};

onMounted(async () => {
  await props.store.loadList();
});

watch(
  () => [route.query],
  async () => {
    isAllSelected.value = false;
    selectedItems.value.clear();
    await props.store.loadList();
  },
  { deep: true },
);
watch(
  () => [props.store.limit],
  async () => {
    if (props.store.setLimit) {
      isAllSelected.value = false;
      selectedItems.value.clear();
      await props.store.loadList();
    }
  },
  { deep: true },
);
</script>

<style lang="scss" scoped>
.container {
  padding-top: 20px;
  padding-left: 10px;
  padding-right: 30px;
  padding-bottom: 20px;
  @media (min-width: 800px) {
    padding-top: 30px;
  }
}
.content {
  padding-top: 25px;
}

.card {
  background: white;
  display: flex;
  flex-direction: column;
  border: 1px solid #e6e7e9;
  border-radius: 4px;
  .hat {
    display: flex;
    flex-direction: column;
    .header {
      padding: 1rem;
      display: flex;
      border-bottom: 1px solid #e6e7e9;
      .title {
        font-size: 115%;
        font-weight: 500;
        @media (max-width: 420px) {
          font-size: 100%;
        }
      }
      .actions {
        position: relative;
        margin-left: auto;
        display: flex;
        gap: 20px;
        padding-right: 10px;
        .add-btn {
          border-radius: 8px;
          border: 1px solid transparent;
          padding: 0.5em 1em;
          font-size: 1em;
          font-weight: 500;
          font-family: inherit;
          cursor: pointer;
          transition: border-color 0.25s;
          color: white;
          background: #206bc4;
          @media (max-width: 320px) {
            font-size: 0.6em;
            padding: 0.5em 0.5em;
          }
          @media (max-width: 440px) {
            font-size: 0.9em;
          }
          @media (min-width: 441px) and (max-width: 500px) {
            font-size: 0.9em;
            padding: 0.7em 1em;
          }
        }
      }
    }
    .filters {
      position: relative;
      display: flex;
      padding-top: 15px;
      padding-bottom: 15px;
      padding-inline: 10px;
      border-bottom: 1px solid #e6e7e9;
      .search {
        margin-left: auto;
        @media (max-width: 500px) {
          margin-left: 0px;
        }
      }
      @media (max-width: 500px) {
        gap: 15px;
        flex-direction: column;
      }
    }
  }
}
.search-btn {
  background: transparent;
  border: 1px solid #e6e7e9;
  border-radius: 0px;
  border-left: none;
}
</style>
