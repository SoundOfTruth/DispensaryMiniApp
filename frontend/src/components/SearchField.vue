<template>
  <div class="filters">
    <div class="search-field">
      <div class="svg">
        <SearchSvg />
      </div>
      <input
        type="text"
        v-model.lazy="pattern"
        :placeholder="props.title"
        class="input-field"
        @keyup.enter="search()"
      />
    </div>
    <slot name="filter"></slot>
  </div>
</template>

<script lang="ts" setup>
import SearchSvg from "./SearchSvg.vue";

import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";

interface inputData {
  title: string;
}

const route = useRoute();
const router = useRouter();
const pattern = ref<string>(route.query.search?.toString() ?? "");

const props = defineProps<inputData>();

const search = () => {
  let query = { ...route.query };
  if (pattern.value) {
    query = { ...query, search: pattern.value };
  }
  router.replace({
    path: route.path,
    query: query,
  });
};
</script>

<style lang="scss" scoped>
.svg {
  padding: 5px 12px;
  width: min-content;
  height: min-content;
}
.filters {
  padding-inline: 25px;
  padding-bottom: 20px;
  display: flex;
  gap: 10px;

  .search-field {
    width: 100%;
    display: flex;
    border: 1px solid #bababa;
    border-radius: 10px;
    padding: 3px;

    .input-field {
      width: 100%;
      border: transparent;
      background: #f5f7fa;
      outline: none;
      box-sizing: border-box;
      color: #bababa;
      font-size: 90%;
    }
  }
}
</style>
