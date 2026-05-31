<template>
  <div class="paginated-page">
    <slot></slot>
    <div class="pagination-container" v-if="count > limit || currentPage < 1 || currentPage > 1">
      <ThePagination :count="count" :limit="limit" :size="3"></ThePagination>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { usePaginationStore } from '@/stores/paginationStore.ts';
import ThePagination from './ThePagination.vue';

import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const paginationStore = usePaginationStore();
const limit = computed(() => paginationStore.limit);

const currentPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});

interface Props {
  count: number;
}
const props = defineProps<Props>();
</script>

<style scoped lang="scss">
.paginated-page {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  padding-bottom: 15px;
  overflow-y: auto;
}
.pagination-container {
  display: flex;
  justify-content: center;
  padding-top: 20px;
  padding-bottom: 20px;
  max-width: 100vw;
  flex-shrink: 0;
  overflow-y: auto;
}
</style>
