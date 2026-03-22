<template>
  <div>
    <aside class="nav-panel">
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
import AdminNavItem from "./AdminNavItem.vue";

const models = [
  {
    title: "Врачи",
    linkName: "admin.doctors",
  },
  {
    title: "Обследования",
    linkName: "admin.doctors",
  },
  {
    title: "Оборудование",
    linkName: "admin.doctors",
  },
];
</script>

<style scoped lang="scss">
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
}
.logout-btn {
  border-radius: 4px;
  padding: 0.4em;
  background: #616876;
  color: white;
  margin-inline: 10px;
}
</style>
