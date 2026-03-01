<template>
  <div>
    <slot></slot>
    <div class="pagination-container">
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
          :disabled="currentPage === props.lastPage"
          @click="goToPage(currentPage + 1)"
        >
          <RightSvg
            class="arrow"
            :class="{ disabled: currentPage == props.lastPage }"
          />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Pagination } from "../utils/pagination";
import LeftSvg from "./svg/LeftSvg.vue";
import RightSvg from "./svg/RightSvg.vue";

interface Props {
  size: number;
  lastPage: number;
}

const props = defineProps<Props>();

const route = useRoute();
const router = useRouter();

const currentPage = ref<number>(1);
const paginationPages = ref<(number | null)[]>();
const pagination = new Pagination(10);

onMounted(() => {
  const page = route.query.page;
  currentPage.value = page ? Number(page) : 1;
  paginationPages.value = pagination.getPages(currentPage.value);
});

const goToPage = (page: number) => {
  if (page >= 1 && page <= props.lastPage && page !== currentPage.value) {
    currentPage.value = page;
    paginationPages.value = pagination.getPages(page);
    router.push({
      path: route.path,
      query: { page: page },
    });
  }
};
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
