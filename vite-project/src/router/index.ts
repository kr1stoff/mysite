import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router"; // 使用类型导入

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/views/Home.vue"),
  },
  // 可以继续添加更多路由
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/views/Settings.vue"),
  },
  {
    path: "/tasks",
    name: "Tasks",
    component: () => import("@/views/Tasks.vue"),
  },
  // ngs
  {
    path: "/ngs/samplesheet",
    name: "IlluminaCreateSamplesheet",
    component: () => import("@/views/ngs/IlluminaCreateSamplesheet.vue"),
  },
  {
    path: "/ngs/lvis",
    name: "LVIS",
    component: () => import("@/views/ngs/LVIS.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 历史模式
  routes, // 将路由规则添加到路由实例中
});

export default router;
