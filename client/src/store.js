import { createStore } from "vuex";

/** @type {import('vuex').StoreOptions} */
const store = {
  state: {
    loading: false,
    isLogin: false,
    isAdmin: false,
    currencyBase: "CAD",
    api: "currency",
  },
  mutations: {
    changeLoginState(state, isLogin) {
      state.isLogin = isLogin;
      state.isAdmin = true;
    },
  },
};

export default createStore(store);
