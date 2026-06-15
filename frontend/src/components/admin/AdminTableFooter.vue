<template>
  <div class="table-footer" v-if="props.store.count">
    <div class="count">Пройденно {{ passedCount }} из {{ props.store.count }} строк</div>
    <div class="right">
      <ThePagination :count="props.store.count" :limit="limit" :size="7"></ThePagination>
      <div class="limit" @click="IsDropdownOpen = !IsDropdownOpen">
        <div>{{ limit }} / на страницу</div>
        <div class="dropdown" v-if="IsDropdownOpen">
          <button class="item" v-for="count in dropdownCount" @click="setLimit(count)">
            {{ count }} / на страницу
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import ThePagination from '../ThePagination.vue';
import type { BaseStore } from '@/stores/base';
import { usePaginationStore } from '@/stores/paginationStore';

const route = useRoute();

const paginationStore = usePaginationStore();
const limit = computed(() => paginationStore.limit);

const setLimit = (count: number) => {
  paginationStore.setLimit(count);
};

const props = defineProps<{
  tableCount: number | undefined;
  store: BaseStore;
}>();

const IsDropdownOpen = ref<boolean>(false);
const dropdownCount = [10, 25, 50, 100];

const currentPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});

const passedCount = computed(() => {
  if (limit.value && props.tableCount !== undefined) {
    return (currentPage.value - 1) * limit.value + props.tableCount;
  }
});
</script>

<style lang="scss" scoped>
.count {
  font-size: 95%;
  color: rgba(97, 104, 118, 1) !important;
  @media (max-width: 500px) {
    display: none;
  }
}
.dropdown {
  position: absolute;
  left: 0;
  bottom: 0;
  border: 1px solid gray;
  border-radius: 4px;
  padding: 4px;
  background: white;
  .item {
    font-weight: 400;
    padding: 4px;
  }
}
.limit {
  position: relative;
  font-size: 90%;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 1px solid black;
  @media (max-width: 500px) {
    display: none;
  }
}
.table-footer {
  display: flex;
  align-items: center;
  background: inherit;
  justify-content: space-between;
  @media (max-width: 500px) {
    justify-content: center;
  }
  .right {
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 90%;
  }
}
</style>
