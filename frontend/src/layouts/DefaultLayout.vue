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
  max-width: 1000px;
  margin: 0 auto;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.content {
  padding-top: 87px;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
</style>
