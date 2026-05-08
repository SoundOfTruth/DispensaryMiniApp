<script setup lang="ts">
import DeleteSvg from "@/components/svg/DeleteSvg.vue";

import { useFilesStore } from "@/stores/files";
import { ref, watch } from "vue";

const emits = defineEmits<{
  (e: "on-select", url: string): void;
}>();
const props = defineProps<{ hidden?: boolean; previewUrl?: string | null }>();

const filesStore = useFilesStore();
const fileInputRef = ref<HTMLInputElement | null>(null);

const fileTypes = ["image/png", "image/jpeg", "image/webp"];
const previewUrl = ref<string | null>();

const clearPreview = () => {
  if (!props.hidden) {
    // if (previewUrl.value) {
    //   URL.revokeObjectURL(previewUrl.value);
    // }
    previewUrl.value = undefined;
    emits("on-select", "");
  }
};

const handleCancel = () => {
  clearPreview();
  if (fileInputRef.value && fileInputRef.value instanceof HTMLInputElement) {
    fileInputRef.value.value = "";
  }
};

const handleFileSelect = async (event: Event) => {
  clearPreview();
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) {
    console.log("no file");
    return;
  }
  if (!fileTypes.some((type) => type == file.type)) {
    console.log(file.type);
    return;
  }
  const created = await filesStore.create(file);
  if (created) {
    emits("on-select", created.url);
    previewUrl.value = created.url;
  }
};

watch(
  () => props.previewUrl,
  (newUrl) => {
    previewUrl.value = newUrl;
  },
);
</script>

<template>
  <input
    type="file"
    @change="handleFileSelect"
    accept="image/*"
    ref="fileInputRef"
    style="display: none"
  />
  <div class="file-input">
    <div v-if="filesStore.loading || previewUrl" @click="handleCancel()">
      <div class="image-wrapper">
        <img :src="previewUrl" class="image" v-if="previewUrl" />
        <div class="loading" v-if="filesStore.loading"></div>
        <div class="deleteOverlay"><DeleteSvg color="white" /></div>
      </div>
    </div>
    <button
      class="choise-btn"
      type="button"
      @click="fileInputRef?.click()"
      :style="hidden ? { display: 'none' } : {}"
    >
      Выбрать файл
    </button>
  </div>
</template>

<style lang="scss" scoped>
.file-input {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 20px;
  .choise-btn {
    padding: 10px 6px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s;
    border: 1px solid black;
  }
}

.image-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  .image {
    width: 60px;
    height: 60px;
    background-size: cover;
    border-radius: 5px;
    border: 1px solid black;
  }
  .loading {
    position: absolute;
    width: 48px;
    height: 48px;
    border: 5px solid black;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    @keyframes rotation {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  }
  .deleteOverlay {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    top: 0;
    left: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s;
    &:hover {
      opacity: 1;
    }
  }
}
</style>
