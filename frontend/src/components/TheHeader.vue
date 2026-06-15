<template>
  <div class="header-wrapper">
    <header>
      <div class="hat">
        <MenuButton @click="toggleMenu()" class="mobile-nav" />
        <RouterLink :to="{ name: indexLink.routeName }" class="link" @click="isMenuOpen = false">
          <h1 class="title">{{ indexLink.title }}</h1>
        </RouterLink>
      </div>
      <nav class="menu mobile-nav" :class="{ active: isMenuOpen }">
        <ul>
          <li @click="toggleMenu()" v-for="link in links" :key="link.routeName">
            <RouterLink :to="{ name: link.routeName }">{{ link.title }}</RouterLink>
          </li>
        </ul>
      </nav>
      <nav class="nav">
        <div class="nav-item" v-for="link in links" :key="link.routeName">
          <RouterLink :to="{ name: link.routeName }">{{ link.title }}</RouterLink>
        </div>
      </nav>
    </header>
    <div class="modal-backdrop" v-if="isMenuOpen" @click="toggleMenu()"></div>
  </div>
</template>

<script setup lang="ts">
import MenuButton from './MenuButton.vue';
import { ref } from 'vue';
import { RouterLink } from 'vue-router';

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
.header-wrapper {
  position: relative;
  z-index: 100;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.1);
  z-index: 99;
}

header {
  z-index: 100;
  background: var(--bg-secondary);
  box-sizing: border-box;
  width: 100%;
  max-width: 1100px;
  border-bottom: 1px solid #d8dee4;
  padding: 20px;
  border-radius: 16px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  box-shadow: 0 1px 10px rgba(0, 0, 0, 0.06);
  position: fixed;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .hat {
    display: flex;
    gap: 30px;
    align-items: center;
  }

  .title {
    color: var(--text-primary);
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
  background: var(--bg-secondary);
  border-bottom: 1px solid #e0e0e0;
  border-radius: 16px;
  margin: 10px;
  z-index: 101;

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
    color: var(--text-primary);
    font-size: 16px;
    transition: background 0.2s ease;

    &:hover {
      background: #f0f0f0;
    }
  }
}
.mobile-nav {
  @media (min-width: 1000px) {
    display: none;
  }
}
.nav {
  display: flex;
  flex-direction: row;
  gap: 20px;
  @media (max-width: 1000px) {
    display: none;
  }
  a {
    display: block;
    padding: 16px;
    text-decoration: none;
    color: var(--text-primary);
    font-size: 110%;
    transition: background 0.2s ease;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
