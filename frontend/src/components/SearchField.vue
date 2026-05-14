<template>
  <div class="search-field">
    <div class="svg">
      <SearchSvg />
    </div>
    <input
      type="text"
      v-model="pattern"
      :placeholder="props.title"
      class="input-field"
      @input="handleSearch()"
    />
  </div>
</template>

<script lang="ts" setup>
import SearchSvg from "./svg/SearchSvg.vue";
import { debounce } from "lodash";
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";

interface inputData {
  title: string;
}

const route = useRoute();
const router = useRouter();
const pattern = ref<string>(route.query.search?.toString() ?? "");

const props = defineProps<inputData>();

const handleSearch = debounce(() => {
  let query = { ...route.query };
  if (pattern.value) {
    query = { ...query, search: pattern.value, page: "1" };
  } else {
    delete query.search;
  }
  router.replace({
    path: route.path,
    query: query,
  });
}, 350);
</script>

<style lang="scss" scoped>
.svg {
  padding: 5px 12px;
  width: min-content;
  height: min-content;
}
.search-field {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  border: 1px solid #bababa;
  border-radius: 10px;
  padding: 3px;
  .input-field {
    width: 100%;
    border: transparent;
    background: transparent;
    outline: none;
    box-sizing: border-box;
    color: #bababa;
    font-size: 90%;
  }
}
</style>
