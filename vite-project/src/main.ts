import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import "element-plus/theme-chalk/index.css";
import ElementPlus from "element-plus";
import "@element-plus/icons-vue";

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.mount("#app");
