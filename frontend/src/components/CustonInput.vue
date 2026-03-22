<template>
  <input
    type="checkbox"
    class="row-select"
    :checked="isChecked"
    @click="emits('onSelect')"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ id?: number; selected?: Set<number> }>();
const emits = defineEmits(["onSelect"]);

const isChecked = computed(() => {
  if (props.id && props.selected) {
    return props.selected.has(props.id);
  }
  return false;
});
</script>

<style lang="scss" scoped>
.row-select {
  background: white;
  border: 1px solid black;
  border-radius: 4px;
  width: 1rem;
  height: 1rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  &:checked[type="checkbox"] {
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8.5l2.5 2.5l5.5 -5.5"/></svg>');
  }
}
</style>
