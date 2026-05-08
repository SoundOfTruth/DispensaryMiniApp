<template>
  <input type="checkbox" :checked="isChecked" @click="emits('onSelect')" />
</template>

<script setup lang="ts">
const props = defineProps<{ id?: number; isChecked?: boolean }>();
const emits = defineEmits(["onSelect"]);
</script>

<style lang="scss" scoped>

</style>
