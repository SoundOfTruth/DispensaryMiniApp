<script setup lang="ts">
import TheHeader from "./components/TheHeader.vue";
</script>

<template>
  <div class="app">
    <TheHeader />
    <div class="content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.app {
  max-width: 900px;
  margin: 0 auto;
}
main {
  margin-top: 16px;
}
.content {
  padding-top: 20px;
  padding-inline: 15px;
  padding-bottom: 20px;
}
</style>
