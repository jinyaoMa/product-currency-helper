import { createRouter, createWebHashHistory } from "vue-router";
import store from "./store.js";
import Login from "./views/Login.vue";
import Settings from "./views/Settings.vue";
import Tokens from "./views/Tokens.vue";
import Home from "./views/Home.vue";
import NotFound from "./views/NotFound.vue";

/** @type {import('vue-router').RouterOptions['routes']} */
const routes = [
  {
    path: "/login",
    component: Login,
    meta: {
      title: "Login | Product Currency Helper",
    },
  },
  {
    path: "/settings",
    component: Settings,
    meta: {
      title: "Settings | Product Currency Helper",
      requireAuth: true,
      requireAuthBasic: true,
    },
  },
  {
    path: "/tokens",
    component: Tokens,
    meta: {
      title: "Access Tokens | Product Currency Helper",
      requireAuth: true,
      requireAuthAdvanced: true,
    },
  },
  {
    path: "/",
    component: Home,
    meta: {
      title: "Home | Product Currency Helper",
      requireAuth: true,
      requireAuthBasic: true,
    },
  },
  {
    path: "/:path(.*)",
    component: NotFound,
    meta: {
      title: "Not Found | Product Currency Helper",
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  if (to.meta.requireAuth && !document.cookie.includes("PCH_PERM=")) {
    next("/login");
    return;
  }
  if (to.meta.requireAuthBasic && !document.cookie.includes("basic:1")) {
    next("/login");
    return;
  }
  if (to.meta.requireAuthAdvanced && !document.cookie.includes("advanced:1")) {
    next("/login");
    return;
  }

  const permission = {
    basic: false,
    manipulation: false,
    advanced: false,
  };
  if (document.cookie.includes("basic:1")) {
    permission.basic = true;
  }
  if (document.cookie.includes("manipulation:1")) {
    permission.manipulation = true;
  }
  if (document.cookie.includes("advanced:1")) {
    permission.advanced = true;
  }
  to.params.permission = permission;

  next();
});

export default router;
