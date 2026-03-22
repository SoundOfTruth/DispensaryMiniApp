<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import ThePagination from "../ThePagination.vue";
import type { BaseStore } from "@/stores/baseStore";

const props = defineProps<{
  tableCount: number | undefined;
  store: BaseStore;
}>();

const route = useRoute();
const router = useRouter();

const IsDropdownOpen = ref<boolean>(false);
const dropdownCount = [10, 25, 50, 100];

const currentPage = computed(() => {
  const page = route.query.page;
  return page ? Number(page) : 1;
});

const passedCount = computed(() => {
  if (props.tableCount) {
    return (currentPage.value - 1) * props.store.limit + props.tableCount;
  }
});

watch(
  () => props.store.limit,
  async () => {
    router.push({ path: route.path, query: { ...route.query, page: 1 } });
    await props.store.loadList();
  },
  { deep: true },
);
</script>

<template>
  <div class="table-footer">
    <div class="count">
      Пройденно {{ passedCount }} из {{ props.store.count }} строк
    </div>
    <div class="right">
      <ThePagination
        :count="props.store.count"
        :limit="props.store.limit"
        :size="7"
      ></ThePagination>
      <div>Лимит</div>
      <div class="limit" @click="IsDropdownOpen = !IsDropdownOpen">
        <div>{{ props.store.limit }} / на страницу</div>
        <div class="dropdown" v-if="IsDropdownOpen">
          <button
            class="item"
            v-for="count in dropdownCount"
            @click="props.store.setLimit(count)"
          >
            {{ count }} / на страницу
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.count {
  font-size: 95%;
  color: rgba(97, 104, 118, 1) !important;
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
  box-shadow:
    0 1px 0 black,
    inset 0 -1px 0 rgba(29, 39, 59, 0.2);
}
.table-footer {
  display: flex;
  align-items: center;
  background: inherit;
  justify-content: space-between;
  .right {
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 90%;
  }
}
</style>
