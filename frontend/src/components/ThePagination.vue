<template>
  <div class="pagination">
    <button
      class="pagination__btn"
      :disabled="currPage === 1"
      @click="goToPage(currPage - 1)"
    >
      <LeftSvg
        class="arrow"
        :class="{ disabled: currPage == 1 }"
        v-if="paginationPages.length > 0"
      />
    </button>

    <div v-for="page in paginationPages">
      <button
        v-if="page != '...'"
        class="pagination__btn"
        :class="{ active: currPage == page }"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>
      <div v-else class="pagination__btn">...</div>
    </div>

    <button
      class="pagination__btn"
      :disabled="currPage === pagesCount"
      @click="goToPage(currPage + 1)"
    >
      <RightSvg
        class="arrow"
        :class="{ disabled: currPage == pagesCount }"
        v-if="paginationPages.length > 0"
      />
    </button>
  </div>
</template>

<script lang="ts" setup>
import LeftSvg from "./svg/LeftSvg.vue";
import RightSvg from "./svg/RightSvg.vue";

import { computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { calcPages } from "@/utils/pagination";

interface Props {
  count: number;
  limit: number;
  size: number;
}

const props = defineProps<Props>();

const route = useRoute();
const router = useRouter();

const pagesCount = computed(() => {
  return Math.ceil(props.count / props.limit);
});
const currPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});
const paginationPages = computed(() => {
  if (pagesCount.value === 0) {
    return [];
  }
  if (pagesCount.value === 1) {
    return [1];
  }
  const endStart = pagesCount.value - props.size;
  if (currPage.value <= props.size) {
    let end = 2 + props.size;
    if (end > pagesCount.value) {
      end = pagesCount.value;
    }
    return calcPages(2, end, pagesCount.value);
  } else if (currPage.value > endStart) {
    return calcPages(endStart, pagesCount.value, pagesCount.value);
  } else {
    const step = Math.trunc(props.size / 2);
    const start = currPage.value - step;
    const end = currPage.value + step + 1;
    return calcPages(start, end, pagesCount.value);
  }
});

const goToPage = (page: number) => {
  router.push({
    path: route.path,
    query: { ...route.query, page: page },
  });
  const element = document.getElementById("scroll-container");
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
};

watch(
  () => [pagesCount.value],
  () => {
    if (currPage.value > pagesCount.value) {
      router.push({
        path: route.path,
        query: { ...route.query, page: pagesCount.value },
      });
    }
  },
);
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  padding: 8px;
  border-radius: 8px;
}

.pagination__btn {
  cursor: pointer;
  padding: 0px;
  width: 40px;
  height: 44px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  border: none;
  border-radius: 8px;
  background: transparent;
  font-size: 16px;
  border: 2px solid transparent;
  &.active {
    border: 2px solid #1e1e1e;
  }
  &:hover {
    background-color: #f3f3f7;
  }
  @media (max-width: 350px) {
    width: 30px;
  }
}

.arrow {
  fill: #39393d;
  &.disabled {
    fill: #dfdee2;
  }
}
</style>
