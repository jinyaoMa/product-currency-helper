<script setup>
import { useStore } from 'vuex'

const store = useStore()

</script>

<template>
  <router-view />
  <div v-if="store.state.loading" class="loading">
    <div class="loading-spinner"></div>
  </div>
</template>

<style>
body {
  margin: 0;
  min-width: 280px;
}

.el-form-item__label {
  font-weight: bold;
}

.el-message {
  min-width: 280px !important;
}
</style>

<style scoped>
.loading {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background-color: #00000099;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99999;
}

@keyframes spinScale {
  0% {
    transform: rotate(0deg) scale(1);
  }

  50% {
    transform: rotate(180deg) scale(1.6);
  }

  100% {
    transform: rotate(360deg) scale(1);
  }
}

.loading-spinner {
  width: 5vmin;
  height: 5vmin;
  border: 1vmin solid #ffffff99;
  box-shadow: 0 0 2px 4px #00000033;
  animation: spinScale 1.6s infinite linear;
  border-radius: 50%;
}
</style>
