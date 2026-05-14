<template>
  <div>
    <RouterLink :to="{ name: routeName }">
      <span class="icon"></span>
      <span class="model-name">{{ title }}</span>
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ title: string; routeName: string }>();
</script>

<style lang="css" scoped>
.model-name {
  text-align: start;
  font-family: inherit;
}
.icon {
  display: inline-block !important;
  height: 20px;
  width: 20px;
}
</style>
