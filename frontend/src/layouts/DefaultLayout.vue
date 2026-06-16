<template>
  <div class="mini-app">
    <TheHeader :index-link="indexLink" :links="links" />
    <div class="content" :class="route.name !== 'index' ? 'content-media' : ''" id="content">
      <RouterView v-slot="{ Component }">
        <TheTransition>
          <Component :is="Component" />
        </TheTransition>
      </RouterView>
    </div>
  </div>
</template>

<script setup lang="ts">
import TheTransition from '@/components/TheTransition.vue';
import TheHeader from '../components/TheHeader.vue';

import { useRoute } from 'vue-router';

const route = useRoute();

interface Link {
  title: string;
  routeName: string;
}
const indexLink = {
  title: 'Клинический онкологический диспансер',
  routeName: 'index',
};
const links: Link[] = [
  {
    title: 'О нас',
    routeName: 'index',
  },
  {
    title: 'Врачи',
    routeName: 'doctors',
  },
  {
    title: 'Обследования',
    routeName: 'inspections',
  },
  {
    title: 'Оборудование',
    routeName: 'equipments',
  },
];
</script>

<style scoped lang="scss">
.mini-app {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.content {
  padding-top: 95px;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
</style>
