import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';

export const usePaginationStore = defineStore('paginationStore', () => {
  const route = useRoute();
  const limit = ref<number>(10);

  const setLimit = (val: number) => {
    limit.value = val;
  };

  const calcPagination = (page: number) => {
    return {
      limit: limit.value,
      offset: (page - 1) * limit.value,
    };
  };

  const page = computed(() => {
    const parsed = Number(route.query.page);

    return parsed > 0 ? parsed : 1;
  });

  const pagination = computed(() => calcPagination(page.value));

  return {
    limit,
    setLimit,
    page,
    calcPagination,
    pagination,
  };
});
