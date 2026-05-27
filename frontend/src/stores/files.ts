import { defineStore } from 'pinia';

import FilesApi from '../api/files';
import { ref } from 'vue';
import { useErrorStore } from './errors';

export const useFilesStore = defineStore('filesStore', () => {
  const loading = ref<boolean>(false);
  const errorStore = useErrorStore();

  const create = async (file: File) => {
    loading.value = true;
    try {
      return await FilesApi.create(file);
    } catch (error) {
      errorStore.parseApiError(error);
    } finally {
      loading.value = false;
    }
  };

  return { loading, create };
});
