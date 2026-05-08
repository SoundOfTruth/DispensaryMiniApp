<template>
  <div>
    <div class="menu-open">
      <MenuButton />
    </div>
    <aside class="nav-panel" v-if="menuOpen">
      <RouterLink class="title" to="/admin"> Панель администратора</RouterLink>
      <nav class="nav">
        <AdminNavItem
          :title="model.title"
          :link-name="model.linkName"
          v-for="model in models"
        />
      </nav>
      <button class="logout-btn">Выйти</button>
    </aside>
  </div>
</template>

<script setup lang="ts">
import MenuButton from "@/components/MenuButton.vue";
import AdminNavItem from "./AdminNavItem.vue";
import { ref } from "vue";

const menuOpen = ref<boolean>(true);

const models = [
  {
    title: "Врачи",
    linkName: "admin.doctors",
  },
  {
    title: "Обследования",
    linkName: "admin.inspections",
  },
  {
    title: "Оборудование",
    linkName: "admin.equipments",
  },
  {
    title: "Типы оборудования",
    linkName: "admin.equipments-types",
  },
  {
    title: "Специальности",
    linkName: "admin.specialties",
  },
  {
    title: "Отделения",
    linkName: "admin.departments",
  },
  {
    title: "Пользователи",
    linkName: "admin.users",
  },
];
</script>

<style scoped lang="scss">
.menu-open {
  padding-top: 16px;
  padding-left: 16px;
  @media (min-width: 800px) {
    display: none;
  }
}
.nav-panel {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  overflow-y: auto;
  width: 15rem;
  background: #1d273b;
  color: #ffffffb3;
  display: flex;
  flex-direction: column;
  .title {
    padding: 15px;
    font-size: 110%;
    text-align: center;
    color: white;
  }
  .nav {
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  @media (max-width: 800px) {
    display: none;
  }
}
.logout-btn {
  border-radius: 4px;
  padding: 0.4em;
  background: #616876;
  color: white;
  margin-inline: 10px;
}
</style>
