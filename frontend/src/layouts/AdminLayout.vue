<template>
  <div class="admin-page">
    <AdminNavigation />
    <div>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminNavigation from "@/components/admin/navigation/AdminNavigation.vue";
</script>

<style scoped lang="scss">
.admin-page {
  margin-left: 15rem;
  @media (max-width: 800px) {
    margin-left: 0px;
  }
}
</style>
