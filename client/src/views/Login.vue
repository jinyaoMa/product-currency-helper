<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { http } from '../http'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const accessToken = ref("")

const login = () => {
  store.state.loading = true
  http.get(`/access/${accessToken.value}`).then((res) => {
    if (res.data.success) {
      router.push("/")
    } else {
      store.state.loading = false
      ElMessage({
        message: "Invalid access token",
        type: "error"
      })
    }
  }).catch(() => {
    store.state.loading = false
    ElMessage({
      message: "Access token should not be empty",
      type: "error"
    })
  })
}
</script>

<template>
  <div class="login">
    <h1 class="title">Product Currency Helper</h1>
    <el-divider class="divider">by Jinyao Ma, 001433428</el-divider>
    <el-form class="form" size="large" label-position="top">
      <el-form-item label="Access Token">
        <el-input type="password" v-model="accessToken" placeholder="Access Token" show-password
          @keyup.enter.native="login" autocomplete />
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
