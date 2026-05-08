<template>
  <input
    class="field"
    v-model="pattern"
    type="text"
    :placeholder="props.title"
    @input="handleSearch()"
    @keydown.enter.prevent
  />
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps<{ title: string }>();

const route = useRoute();
const router = useRouter();

const pattern = ref<string | undefined>(
  route.query.search as string | undefined,
);

const handleSearch = () => {
  let query = { ...route.query };
  if (pattern.value) {
    query = { search: pattern.value };
  } else {
    delete query.search;
  }
  router.replace({
    path: route.path,
    query: query,
  });
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
</style>
