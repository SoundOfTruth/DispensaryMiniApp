<template>
  <div>
    <li v-for="link in links" :key="link.routeName">
      <RouterLink :to="{ name: link.routeName }">{{ link.title }}</RouterLink>
    </li>
  </div>
</template>

<script lang="ts" setup>
import { RouterLink } from 'vue-router';

interface Link {
  title: string;
  routeName: string;
}
const props = defineProps<{ indexLink: Link; links: Link[] }>();
</script>
