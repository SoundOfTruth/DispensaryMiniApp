import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { defineStore } from "pinia";

import UserApi from "@/api/users";
import { parseApiErrors, type ApiError } from "@/utils/api";

interface ApiParams {
  limit: number;
  offset: number;
  search?: number;
}

interface Filters {
  page?: number;
  search?: string;
}

import type { CreateUser, User } from "@/types/users";
import { useAuthStore } from "./auth";

export const useUserStore = defineStore("userStore", () => {
  const authStore = useAuthStore();
  const route = useRoute();

  const currentUser = ref<User>();
  const isAdmin = computed(
    () =>
      currentUser.value?.role === "superuser" ||
      currentUser.value?.role === "admin",
  );
  const users = ref<User[]>([]);
  const user = ref<User>();

  const count = ref<number>(0);
  const limit = ref<number>(10);
  const errors = ref<ApiError[]>([]);

  const setLimit = (val: number) => {
    limit.value = val;
  };

  const getAllowedParams = (filters: Filters): ApiParams => {
    const allowedParams: (keyof Filters)[] = ["search"];
    const page = filters?.page || 1;
    const params: ApiParams = {
      offset: (page - 1) * limit.value,
      limit: limit.value,
    };
    Object.entries(filters).forEach(([key, value]) => {
      const param = key as keyof Filters;

      if (
        param != "page" &&
        allowedParams.includes(param) &&
        value !== undefined &&
        value !== null
      ) {
        params[param] = value;
      }
    });
    return params;
  };

  const loadCurrentUser = async () => {
    errors.value = [];
    if (authStore.isAuthenticated) {
      try {
        currentUser.value = await UserApi.getMe();
      } catch (error) {
        errors.value = parseApiErrors(error);
      }
    }
  };

  const loadList = async () => {
    errors.value = [];
    const params = getAllowedParams(route.query);
    try {
      const paginatedData = await UserApi.getAll(params);
      users.value = paginatedData.results;
      count.value = paginatedData.count;
      if (paginatedData.count == 0 && params.search) {
        errors.value = [
          { message: "Ничего не найдено по заданным параметрам." },
        ];
      }
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const loadById = async (id: number) => {
    errors.value = [];
    try {
      user.value = await UserApi.get(id);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteById = async (id: number) => {
    try {
      await UserApi.delete(id);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const deleteList = async (ids: number[]) => {
    try {
      await UserApi.deleteBulk(ids);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const create = async (data: CreateUser) => {
    try {
      return await UserApi.create(data);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
  };

  const update = async (id: number, data: Partial<CreateUser>) => {
    try {
      return await UserApi.update(id, data);
    } catch (error) {
      errors.value = parseApiErrors(error);
    }
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
    errors,
    loadCurrentUser,
    loadById,
    loadList,
    setLimit,
    create,
    update,
    deleteById,
    deleteList,
    logout,
  };
});
