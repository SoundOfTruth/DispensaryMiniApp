<template>
  <div :class="isAdmin ? 'admin-page' : ''">
    <AdminNavigation :links="links" />
    <TheHeader :index-link="indexLink" :links="links" class="mobile-nav" />
    <div class="content" id="content">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminNavigation from "@/components/admin/navigation/AdminNavigation.vue";
import { computed } from "vue";

import { useUserStore } from "@/stores/users";

import TheHeader from "../components/TheHeader.vue";

interface Link {
  title: string;
  routeName: string;
}
const indexLink = {
  title: "Admin app",
  routeName: "admin.index",
};
const links: Link[] = [
  {
    title: "Врачи",
    routeName: "admin.doctors",
  },
  {
    title: "Обследования",
    routeName: "admin.inspections",
  },
  {
    title: "Оборудование",
    routeName: "admin.equipments",
  },
  {
    title: "Типы оборудования",
    routeName: "admin.equipments-types",
  },
  {
    title: "Специальности",
    routeName: "admin.specialties",
  },
  {
    title: "Отделения",
    routeName: "admin.departments",
  },
  {
    title: "Пользователи",
    routeName: "admin.users",
  },
];
const userStore = useUserStore();
const isAdmin = computed(() => userStore.isAdmin);
</script>

<style scoped lang="scss">
.admin-page {
  margin-left: 15rem;
  @media (max-width: 800px) {
    margin-left: 0px;
  }
}
.mobile-nav {
  @media (min-width: 800px) {
    display: none;
  }
}
.desctop.nav {
  @media (max-width: 800px) {
    display: none;
  }
}
.content {
  padding-top: 25px;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  @media (min-width: 800px) {
    padding-top: 0px;
  }
}
</style>
