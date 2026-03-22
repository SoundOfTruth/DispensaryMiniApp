<template>
  <div class="card">
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <td class="s-coll">
              <CustonInput v-model="isAllSelected" @on-select="selectAll()" />
            </td>
            <td class="s-coll"></td>
            <th v-for="col in columns">{{ col.text }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in data">
            <td>
              <CustonInput
                :id="row.id"
                :selected="selectedItems"
                @on-select="selectOne(row.id)"
              />
            </td>
            <td>
              <RowActions />
            </td>
            <td v-for="col in columns">
              {{ row[col.key as keyof typeof row] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <AdminTableFooter :table-count="data?.length" :store="store" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import RowActions from "./RowActions.vue";
import CustonInput from "../CustonInput.vue";
import AdminTableFooter from "./AdminTableFooter.vue";
import type { BaseStore } from "../../stores/baseStore";

const isAllSelected = ref<boolean>(false);

interface Columns {
  key: string;
  text: string;
}

interface Props {
  columns: Columns[];
  data: any[] | undefined;
  store: BaseStore;
}

const props = defineProps<Props>();

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
</style>
