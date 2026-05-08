import { createWebHistory, createRouter } from "vue-router";

import { publicRoutes } from "./public";
import { adminRoutes } from "./admin";

export const router = createRouter({
  history: createWebHistory(),
  routes: [adminRoutes, publicRoutes],
});

router.beforeEach((to, _from, next) => {
  const pageQuery = to.query.page;
  const page = Number(pageQuery);
  if (pageQuery && (page < 1 || isNaN(page))) {
    next({
      ...to,
      query: { ...to.query, page: 1 },
    });
  } else {
    next();
  }
});
