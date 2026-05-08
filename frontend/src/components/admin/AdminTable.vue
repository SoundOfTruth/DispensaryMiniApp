<template>
  <div class="card">
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <td class="s-coll">
              <input
                type="checkbox"
                @click="emits('selectAll')"
                :checked="isAllSelected"
              />
            </td>
            <td class="s-coll"></td>
            <th v-for="col in columns">{{ col.text }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in data">
            <td>
              <input
                type="checkbox"
                @click="emits('selectOne', row.id)"
                :checked="selectedItems.has(row.id)"
              />
            </td>
            <td>
              <div class="row-actions">
                <RouterLink
                  class="action-btn"
                  :to="{
                    name: routeName + '.detail',
                    params: { id: row.id },
                  }"
                >
                  <WatchSvg />
                </RouterLink>
                <RouterLink
                  class="action-btn"
                  :to="{
                    name: routeName + '.edit',
                    params: { id: row.id },
                  }"
                >
                  <EditSvg />
                </RouterLink>
                <button class="action-btn" @click="emits('openDelete', row.id)">
                  <DeleteSvg />
                </button>
              </div>
            </td>
            <td v-for="col in columns">
              {{
                col.secondKey
                  ? row[col.key as keyof typeof row]?.[col.secondKey]
                  : row[col.key as keyof typeof row]
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <AdminTableFooter :table-count="data?.length" :store="store" />
  </div>
</template>

<script lang="ts" setup>
import DeleteSvg from "../svg/DeleteSvg.vue";
import EditSvg from "../svg/EditSvg.vue";
import WatchSvg from "../svg/WatchSvg.vue";
import AdminTableFooter from "./AdminTableFooter.vue";

import { useRoute } from "vue-router";

const route = useRoute();

const routeName = String(route.name);

import type { BaseStore } from "../../stores/base";

interface Columns {
  key: string;
  text: string;
  secondKey?: string | string;
}

interface Props {
  columns: Columns[];
  data: any[] | undefined;
  store: BaseStore;
  isAllSelected: boolean;
  selectedItems: Set<number>;
}

const props = defineProps<Props>();
const emits = defineEmits(["openDelete", "selectAll", "selectOne"]);
</script>

<style lang="scss" scoped>
.card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border: 1px solid rgba(0, 0, 21, 0.175);
  border-radius: 0.375rem;
}
.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  table {
    caption-side: bottom;
    border-collapse: collapse;
    width: 100%;
    border-color: #d8dbe0;
    border-bottom-width: 1px;
    vertical-align: top;
    margin-bottom: 1rem;
  }
  th {
    text-align: start;
  }
  .s-coll {
    width: 0.25rem;
  }
}

tbody,
td,
tfoot,
th,
thead,
tr {
  border-color: inherit;
  border-style: solid;
  border-width: 0;
}

.table > :not(caption) > * > * {
  padding: 0.5rem 0.5rem;
  background-color: var(--cui-table-bg);
  border-bottom-width: 1px;
}
.table {
  width: 100%;
  margin-bottom: 1rem;
  vertical-align: top;
  border-color: var(--cui-table-border-color);
}

.row-actions {
  display: flex;
  place-content: center;
  .action-btn {
    width: 20px;
    display: flex;
    align-items: center;
    background: transparent;
    padding: 0;
    &:hover {
      border-color: transparent !important;
    }
    &:focus,
    &:focus-visible {
      outline: none !important;
    }
  }
}
</style>
