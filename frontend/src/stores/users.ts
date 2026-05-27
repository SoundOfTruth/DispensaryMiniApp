import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

import UserApi from '@/api/users';

import type { CreateUser, User } from '@/types/users';
import { useAuthStore } from './auth';
import { useErrorStore } from './errors';
import type { ApiParams } from '@/api/base';

export const useUserStore = defineStore('userStore', () => {
  const authStore = useAuthStore();
  const errorStore = useErrorStore();
  const route = useRoute();

  const currentUser = ref<User>();
  const isAdmin = computed(
    () => currentUser.value?.role === 'superuser' || currentUser.value?.role === 'admin'
  );
  const users = ref<User[]>([]);
  const user = ref<User>();

  const count = ref<number>(0);
  const limit = ref<number>(10);

  const setLimit = (val: number) => {
    limit.value = val;
  };

  const getRouteParams = (): ApiParams => {
    const routeSearch = route.query.search;
    const search = routeSearch ? String(routeSearch) : undefined;
    const page = Number(route.query.page) || 1;
    return {
      offset: (page - 1) * limit.value,
      limit: limit.value,
      search: search ? search : undefined,
    };
  };

  const loadCurrentUser = async () => {
    if (authStore.isAuthenticated) {
      try {
        currentUser.value = await UserApi.getMe();
      } catch (error) {
        errorStore.parseApiError(error);
      }
    }
  };

  const loadList = async () => {
    const params = getRouteParams();
    try {
      const paginatedData = await UserApi.getAll(params);
      users.value = paginatedData.results;
      count.value = paginatedData.count;
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const loadById = async (id: number) => {
    try {
      user.value = await UserApi.get(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await UserApi.delete(id);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await UserApi.deleteBulk(ids);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const create = async (data: CreateUser) => {
    try {
      return await UserApi.create(data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const update = async (id: number, data: Partial<CreateUser>) => {
    try {
      return await UserApi.update(id, data);
    } catch (error) {
      errorStore.parseApiError(error);
    }
  };

  const changePassword = async (currentPassword: string, newPassword: string) => {
    return await UserApi.changePassword(currentPassword, newPassword);
  };

  const logout = async () => {
    currentUser.value = undefined;
    await authStore.logout();
  };

  return {
    currentUser,
    isAdmin,
    user,
    users,
    count,
    limit,
    loadCurrentUser,
    loadById,
    loadList,
    setLimit,
    create,
    update,
    deleteById,
    deleteList,
    logout,
    changePassword,
  };
});
