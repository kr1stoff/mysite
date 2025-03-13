import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// 配置不同环境的变量
export default defineConfig(({ mode }) => {
  // * 项目目录中的 .env 文件配置
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [vue()],
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        // * 配置请求代理到 FastAPI
        "^/api/(ngs|settings)": {
          target: env.VITE_API_HOST,
          changeOrigin: true,
          rewrite: (path) => path,  // 路径相同无需修改
        },
        // * 配置请求代理到 NGINX
        "/api/templates": {
          target: env.VITE_NGINX_HOST,
          changeOrigin: true,
          rewrite: (path) => path,
        },
      },
    },
    build: {
      outDir: "dist",
      rollupOptions: {
        input: {
          main: "index.html",
        },
      },
    },
    resolve: {
      // 配置路径别名，将 @ 指向 src 目录
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    css: {
      preprocessorOptions: {
        scss: { api: "modern-compiler" },
      },
    },
  };
});
