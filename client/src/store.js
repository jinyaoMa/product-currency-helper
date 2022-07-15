import { createStore } from "vuex";

/** @type {import('vuex').StoreOptions} */
const store = {
  state: {
    loading: false,
    base: "",
    api: "",
  },
};

export default createStore(store);
