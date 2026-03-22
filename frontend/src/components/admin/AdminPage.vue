<template>
  <div class="container">
    <div class="card">
      <div class="hat">
        <div class="header">
          <div class="title">{{ props.title }}</div>
          <div class="actions">
            <ExportButton />
            <button class="add-btn">{{ props.addButtonName }}</button>
          </div>
        </div>
        <div class="filters">
          <ActionButton />
          <div class="search">
            <SearchField title="Поиск" />
          </div>
        </div>
      </div>
    </div>
    <div class="content">
      <AdminTable :columns="props.columns" :data="props.data" :store="store" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import ActionButton from "./ActionButton.vue";
import AdminTable from "./AdminTable.vue";
import SearchField from "../SearchField.vue";
import ExportButton from "./ExportButton.vue";
import type { BaseStore } from "../../stores/baseStore";

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

const props = defineProps<inputData>();
</script>

<style lang="scss" scoped>
.container {
  padding-top: 50px;
  padding-left: 10px;
  padding-right: 30px;
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
      align-items: center;
      border-bottom: 1px solid #e6e7e9;
      .title {
        font-size: 115%;
        font-weight: 500;
      }
      .actions {
        position: relative;
        margin-left: auto;
        display: flex;
        gap: 20px;
        padding-right: 10px;
        .export-btn {
          color: white;
          background: #616876;
        }
        .add-btn {
          color: white;
          background: #206bc4;
        }
      }
    }
    .filters {
      position: relative;
      display: flex;
      padding: 15px;
      border-bottom: 1px solid #e6e7e9;
      .search {
        margin-left: auto;
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
