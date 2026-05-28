type PaginationPage = number | '...';

import { useRoute } from 'vue-router';
import { computed } from 'vue';

export const calcPages = (start: number, end: number, pagesCount: number): PaginationPage[] => {
  const pages: PaginationPage[] = [1];

  if (start < 4) {
    start = 2;
  } else {
    pages.push('...');
  }
  if (pagesCount - end == 1) {
    end = pagesCount;
  }
  for (let i = start; i < end; i++) {
    pages.push(i);
  }
  if (end != pagesCount) {
    pages.push('...');
  }
  pages.push(pagesCount);
  return pages;
};

export function usePagination(limit = 10) {
  const route = useRoute();

  const calcPagination = (page: number) => {
    return {
      limit,
      offset: (page - 1) * limit,
    };
  };

  const page = computed(() => {
    const parsed = Number(route.query.page);

    return parsed > 0 ? parsed : 1;
  });

  const pagination = computed(() => calcPagination(page.value));

  return {
    page,
    calcPagination,
    pagination,
  };
}
