<template>
  <div class="item-search">
    <input
      class="field"
      v-model="searchPattern"
      type="text"
      placeholder="Найти обследование"
      @input="handleSearch"
      @keydown.enter.prevent
    />
  </div>
  <div @scroll="handleScroll" class="selection">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { debounce } from "lodash";
import { computed, ref } from "vue";

interface Filters {
  page?: number;
  search?: string;
}

const props = defineProps<{ count: number; limit: number }>();
const emits = defineEmits<{
  (e: "load", filters: Filters): Promise<void>;
  (e: "search", search: string): Promise<void>;
}>();

const searchPattern = ref<string>("");

const pagesCount = computed(() => {
  return Math.ceil(props.count / props.limit);
});
const currPage = ref<number>(1);

const handleSearch = debounce(async () => {
  currPage.value = 1;
  await emits("search", searchPattern.value);
}, 350);

const handleScroll = async (event: Event) => {
  const target = event.target as HTMLElement;
  if (
    Math.ceil(target.scrollTop + target.clientHeight) >= target.scrollHeight
  ) {
    console.log("da");
    if (currPage.value < pagesCount.value) {
      currPage.value += 1;
      await emits("load", {
        page: currPage.value,
        search: searchPattern.value ? searchPattern.value : undefined,
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.field {
  width: 100%;
  padding: 10px 0;
  text-indent: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
}

.item-search {
  margin-bottom: 16px;
}
.selection {
  box-sizing: border-box;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 16px;
  .item {
    display: flex;
    width: 100%;
    padding: 12px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background-color 0.2s;
    &:hover {
      background-color: #f8f9fa;
    }
  }
}
</style>
