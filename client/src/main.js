import { createApp } from "vue";
import App from "./App.vue";
import store from "./store.js";
import routes from "./routes.js";

createApp(App).use(store).use(routes).mount("#app");
