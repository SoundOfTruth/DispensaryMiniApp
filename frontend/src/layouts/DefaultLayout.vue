<template>
  <div class="mini-app">
    <TheHeader :index-link="indexLink" :links="links" />
    <div class="content" id="content">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import TheHeader from "../components/TheHeader.vue";

interface Link {
  title: string;
  routeName: string;
}
const indexLink = {
  title: "Клинический онкологический диспансер",
  routeName: "index",
};
const links: Link[] = [
  {
    title: "О нас",
    routeName: "index",
  },
  {
    title: "Врачи",
    routeName: "doctors",
  },
  {
    title: "Обследования",
    routeName: "inspections",
  },
  {
    title: "Оборудование",
    routeName: "equipments",
  },
];
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
