<template>
  <div class="filters">
    <div class="search-field">
      <div class="svg">
        <SearchSvg />
      </div>
      <input type="text" :placeholder="props.title" class="input-field" />
    </div>
    <FilterButton/>
  </div>
</template>

<script lang="ts" setup>
import FilterButton from "./FilterButton.vue";
import SearchSvg from "./SearchSvg.vue";

interface inputData {
  title: string;
}
const props = defineProps<inputData>();
</script>

<style lang="scss" scoped>
.svg {
  padding: 5px 12px;
  width: min-content;
  height: min-content;
}
.filters {
  padding-inline: 10px;
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
