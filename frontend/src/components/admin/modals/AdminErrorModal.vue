<template>
  <CenterModal :open="props.errors.length > 0" @close="emits('close')">
    <div>
      <div class="title">Ошибка</div>
    </div>
    <ul>
      <li v-for="(err, i) in errors" :key="i">
        <span v-if="err.field">
          <b>{{ err.field }}</b
          >: {{ err.message }}
        </span>
        <span v-else>
          {{ err.message }}
        </span>
      </li>
    </ul>
  </CenterModal>
</template>

<script lang="ts" setup>
import { type ApiError } from "@/utils/api";
import CenterModal from "./CenterModal.vue";

const props = defineProps<{
  errors: ApiError[];
}>();

const emits = defineEmits(["close"]);
</script>

<style lang="scss" scoped>
.title {
  padding-top: 15px;
  text-align: center;
  font-size: 110%;
  font-weight: 500;
}
</style>
