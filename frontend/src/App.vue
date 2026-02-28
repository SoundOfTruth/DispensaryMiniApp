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
  <div id="modals"></div>
</template>

<style scoped>
main {
  margin-top: 16px;
}
.app {
  max-width: 900px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0px;
}
</style>
