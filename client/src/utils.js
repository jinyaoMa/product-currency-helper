export const storage = {
  loadSettings(settings) {
    if (window && window.localStorage) {
      let base = window.localStorage.getItem("PCH_BASE");
      if (base) {
        settings.base = base;
      }
      let api = window.localStorage.getItem("PCH_API");
      if (api) {
        settings.api = api;
      }
    }
  },
  saveSettings(settings) {
    if (window && window.localStorage) {
      if (settings.base) {
        window.localStorage.setItem("PCH_BASE", settings.base);
      }
      if (settings.api) {
        window.localStorage.setItem("PCH_API", settings.api);
      }
    }
  },
};
