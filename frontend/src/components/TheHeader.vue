<template>
  <header>
    <div class="hat">
      <MenuButton @click="toggleMenu()" />
      <RouterLink
        :to="{ name: indexLink.routeName }"
        class="link"
        @click="isMenuOpen = false"
        ><h1 class="title">{{ indexLink.title }}</h1></RouterLink
      >
    </div>
    <nav class="menu" :class="{ active: isMenuOpen }">
      <ul>
        <li @click="toggleMenu()" v-for="link in links">
          <RouterLink :to="{ name: link.routeName }">{{
            link.title
          }}</RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup lang="ts">
import MenuButton from "./MenuButton.vue";

import { ref } from "vue";
import { RouterLink } from "vue-router";

interface Link {
  title: string;
  routeName: string;
}
const props = defineProps<{ indexLink: Link; links: Link[] }>();

const isMenuOpen = ref<boolean>(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style scoped lang="scss">
header {
  box-sizing: border-box;
  width: 100%;
  max-width: 1000px;
  border-bottom: 1px solid black;
  padding: 16px;
  position: fixed;
  top: 0;
  z-index: 100;
  background: #f5f7fa;
  .hat {
    display: flex;
    gap: 30px;
    align-items: center;
  }
  .title {
    color: #222;
    font-size: 140%;
    font-weight: 500;
    margin: 0;
    padding: 0;
    line-height: 0.8;
    max-width: 275px;
  }
}

.menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid #e0e0e0;
  &.active {
    display: block;
  }
  ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  li {
    border-bottom: 1px solid #f0f0f0;
  }
  a {
    display: block;
    padding: 16px;
    text-decoration: none;
    color: black;
    font-size: 16px;
    transition: background 0.2s black;
  }
}

@media (max-width: 768px) {
  .header-title {
    font-size: 16px;
    padding: 0 50px;
  }
}
</style>
