<template>
  <div class="admin-page">
    <AdminNavigation />
    <div>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminNavigation from "../components/admin/AdminNavigation.vue";
</script>

<style scoped lang="scss">
.admin-page {
  margin-left: 15rem;
}
</style>
