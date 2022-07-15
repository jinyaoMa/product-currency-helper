import { createApp } from "vue";
import App from "./App.vue";
import store from "./store.js";
import routes from "./routes.js";
import "element-plus/es/components/message/style/css";

createApp(App).use(store).use(routes).mount("#app");
