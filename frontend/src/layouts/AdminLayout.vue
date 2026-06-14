<template>
  <div :class="isAdmin ? 'admin-page' : ''">
    <AdminNavigation :links="links" v-if="isAdmin" />
    <TheHeader
      :index-link="indexLink"
      :links="links"
      class="mobile-nav"
      v-if="isAdmin"
    />
    <div class="content" id="content">
      <RouterView v-slot="{ Component }">
        <TheTransition>
          <Component :is="Component" />
        </TheTransition>
      </RouterView>
    </div>
  </div>
</template>

<script setup lang="ts">
import TheHeader from "../components/TheHeader.vue";
import TheTransition from "@/components/TheTransition.vue";
import AdminNavigation from "@/components/admin/navigation/AdminNavigation.vue";

import { computed } from "vue";
import { useUserStore } from "@/stores/users";

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
  @media (max-width: 950px) {
    margin-left: 0px;
  }
}
.mobile-nav {
  @media (min-width: 950px) {
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
  @media (min-width: 950px) {
    padding-top: 0px;
  }
}
</style>
