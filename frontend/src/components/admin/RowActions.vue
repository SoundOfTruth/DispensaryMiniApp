<template>
  <div class="row-actions">
    <button><WatchSvg /></button>
    <button><EditSvg /></button>
    <button><DeleteSvg /></button>
  </div>
</template>

<script setup lang="ts">
import DeleteSvg from "../svg/DeleteSvg.vue";
import EditSvg from "../svg/EditSvg.vue";
import WatchSvg from "../svg/WatchSvg.vue";

const emits = defineEmits(["watch", "edit", "delete"]);
</script>

<style lang="scss" scoped>
.row-actions {
  display: flex;
  place-content: center;
  button {
    width: 20px;
    display: flex;
    align-items: center;
    background: transparent;
    padding: 0;
    &:hover {
      border-color: transparent !important;
    }
    &:focus,
    &:focus-visible {
      outline: none !important;
    }
  }
}
</style>
