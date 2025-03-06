import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// 配置不同环境的变量
export default defineConfig(({ mode }) => {
  // ! 项目目录中的 .env 文件配置
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [vue()],
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        "/api/ngs": {
          target: env.VITE_API_HOST,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/ngs/, "/api/ngs"),
        },
        "/api/template": {
          target: env.VITE_NGINX_HOST,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/template/, "/api/template"),
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
