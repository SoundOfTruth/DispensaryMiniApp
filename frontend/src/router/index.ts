import { createWebHistory, createRouter } from "vue-router";

import { publicRoutes } from "./public";
import { adminRoutes } from "./admin";
import { useUserStore } from "@/stores/users";

export const router = createRouter({
  history: createWebHistory(),
  routes: [adminRoutes, publicRoutes],
});

router.beforeEach(async (to, _from, next) => {
  const pageQuery = to.query.page;
  const page = Number(pageQuery);
  const userStore = useUserStore();

  if (to.name?.toString().includes("admin")) {
    if (!userStore.currentUser) {
      await userStore.loadCurrentUser();
    }
    if (!userStore.isAdmin && to.name != "admin.login") {
      next({ name: "admin.login" });
      return;
    } else if (userStore.isAdmin && to.name == "admin.login") {
      next({ name: "admin.index" });
      return;
    }
  }

  if (pageQuery && (page < 1 || isNaN(page))) {
    next({
      ...to,
      query: { ...to.query, page: 1 },
    });
    return;
  }
  next();
});
