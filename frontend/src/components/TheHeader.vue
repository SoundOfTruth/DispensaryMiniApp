<template>
  <header>
    <div class="hat">
      <button class="menu-button" @click="toggleMenu()">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <RouterLink to="/"
        ><h1 class="title">Клинический онкологический диспансер</h1></RouterLink
      >
    </div>
    <nav class="menu" :class="{ active: isMenuOpen }">
      <ul>
        <li @click="toggleMenu()">
          <RouterLink to="/">О нас</RouterLink>
        </li>
        <li @click="toggleMenu()">
          <RouterLink to="/doctors">Врачи</RouterLink>
        </li>
        <li @click="toggleMenu()">
          <RouterLink to="/inspections">Обследования</RouterLink>
        </li>
        <li @click="toggleMenu()">
          <RouterLink to="/equipments">Оборудование</RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

const isMenuOpen = ref<boolean>(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style scoped>
header {
  border-bottom: 1px solid black;
  padding-inline: 16px;
  padding-top: 12px;
  padding-bottom: 16px;
  position: sticky;
  top: 0;
  z-index: 100;
  background: #f5f7fa;
}

header .hat {
  display: flex;
  gap: 30px;
}

header .title {
  color: #222;
  font-size: 140%;
  font-weight: 500;
  margin: 0;
  padding: 0;
  line-height: 0.8;
  max-width: 275px;
}

.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 8px;
}

.menu-button span {
  width: 24px;
  height: 2px;
  background: #222;
  display: block;
  transition: all 0.3s black;
}

.menu-button.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.menu-button.active span:nth-child(2) {
  opacity: 0;
}

.menu-button.active span:nth-child(3) {
  transform: rotate(-45deg) translate(8px, -8px);
}

.menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.menu.active {
  display: block;
}

.menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu li {
  border-bottom: 1px solid #f0f0f0;
}

.menu a {
  display: block;
  padding: 16px;
  text-decoration: none;
  color: #222;
  font-size: 16px;
  transition: background 0.2s black;
}

@media (max-width: 768px) {
  .header-title {
    font-size: 16px;
    padding: 0 50px;
  }
}
</style>
