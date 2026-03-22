<template>
  <div>
    <slot></slot>
    <div
      class="pagination-container"
      v-if="count > limit || currentPage < 1 || currentPage > 1"
    >
      <ThePagination :count="count" :limit="limit" :size="3"></ThePagination>
    </div>
  </div>
</template>

<script lang="ts" setup>
import ThePagination from "./ThePagination.vue";

import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const currentPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});

interface Props {
  count: number;
  limit: number;
}
const props = defineProps<Props>();
</script>

<style scoped lang="scss">
.pagination-container {
  display: flex;
  justify-content: center;
  padding-top: 30px;
  padding-bottom: 30px;
  max-width: 100vw;
  overflow-x: hidden;
}
</style>
