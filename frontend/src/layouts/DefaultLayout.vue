<template>
  <div class="mini-app">
    <TheHeader />
    <div class="content" id="content">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import TheHeader from "../components/TheHeader.vue";
</script>

<style scoped>
.mini-app {
  max-width: 900px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.content {
  flex: 1;
  overflow-y: auto;
}
</style>
