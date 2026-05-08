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
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
</style>
