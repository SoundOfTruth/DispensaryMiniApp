import { defineStore } from "pinia";

import FilesApi from "../api/files";
import { ref } from "vue";
import { parseApiErrors } from "@/utils/api";

export const useFilesStore = defineStore("filesStore", () => {
  const loading = ref<boolean>(false);

  const create = async (file: any) => {
    loading.value = true;
    try {
      return await FilesApi.create(file);
    } catch (error) {
      parseApiErrors(error);
    } finally {
      loading.value = false;
    }
  };

  return { loading, create };
});
