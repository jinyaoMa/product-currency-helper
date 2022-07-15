<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const form = reactive({
  accessToken: ""
})

const login = () => {
  console.log('login!')
  store.commit('changeLoginState', true)
  router.push("/")
}
</script>

<template>
  <div class="login">
    <h1 class="title">Product Currency Helper</h1>
    <el-divider class="divider">by Jinyao Ma, 001433428</el-divider>
    <el-form class="form" size="large" label-position="top" :model="form">
      <el-form-item label="Access Token">
        <el-input type="password" v-model="form.accessToken" placeholder="Access Token" show-password
          @keyup.enter.native="login" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

@media (min-width: 420px) {
  .login {
    justify-content: center;
  }
}

.title {
  color: #337ecc;
  text-shadow: 2px 2px #7ebeff;
}

.title,
.divider {
  text-align: center;
}

.form {
  margin-top: 1.3em;
  width: 240px;
  padding: 20px 20px 0;
  background-color: #fafbfc;
}
</style>
