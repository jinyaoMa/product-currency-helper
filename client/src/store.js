import { createStore } from "vuex";

/** @type {import('vuex').StoreOptions} */
const store = {
  state: {
    loading: false,
    isLogin: false,
    isAdmin: false,
    currencyBase: "",
    threshold: 0.0,
  },
  mutations: {
    changeLoginState(state, isLogin) {
      state.isLogin = isLogin;
      state.isAdmin = true;
    },
  },
};

export default createStore(store);
