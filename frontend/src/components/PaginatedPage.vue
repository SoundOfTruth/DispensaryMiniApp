<template>
  <div>
    <slot></slot>
    <div class="pagination-container" v-if="pagesCount > 1">
      <div class="pagination">
        <button
          class="pagination__btn"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        >
          <LeftSvg class="arrow" :class="{ disabled: currentPage == 1 }" />
        </button>

        <div v-for="page in paginationPages">
          <button
            v-if="page"
            class="pagination__btn"
            :class="{ active: currentPage == page }"
            @click="goToPage(page)"
          >
            {{ page ? page : "..." }}
          </button>
          <div v-else class="pagination__btn">...</div>
        </div>

        <button
          class="pagination__btn"
          :disabled="currentPage === props.pagesCount"
          @click="goToPage(currentPage + 1)"
        >
          <RightSvg
            class="arrow"
            :class="{ disabled: currentPage == props.pagesCount }"
          />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, computed, useTemplateRef } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Pagination } from "../utils/pagination";
import LeftSvg from "./svg/LeftSvg.vue";
import RightSvg from "./svg/RightSvg.vue";

interface Props {
  pagesCount: number;
}

const props = defineProps<Props>();

const route = useRoute();
const router = useRouter();

const paginationPages = ref<(number | null)[]>();

const currentPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});

onMounted(() => {
  const pagination = new Pagination(props.pagesCount);
  paginationPages.value = pagination.getPages(currentPage.value);
});

const goToPage = (page: number) => {
  if (page >= 1 && page <= props.pagesCount && page !== currentPage.value) {
    router.push({
      path: route.path,
      query: { page: page },
    });

    const element = document.getElementById("scroll-container");
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  }
};

watch(
  () => [props.pagesCount, route.query],
  () => {
    const pagination = new Pagination(props.pagesCount);
    paginationPages.value = pagination.getPages(currentPage.value);
  },
);
</script>

<style scoped lang="scss">
.pagination-container {
  display: flex;
  justify-content: center;
  padding-top: 30px;
  padding-bottom: 30px;
}
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
}

.arrow {
  fill: #39393d;
  &.disabled {
    fill: #dfdee2;
  }
}
</style>
