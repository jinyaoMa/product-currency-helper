<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { http } from '../http'
import { storage } from '../utils'

const store = useStore()
const router = useRouter()

const baseOptions = ref([])
const apiOptions = ref([])

const settings = reactive({
  base: "",
  api: ""
})

onMounted(async () => {
  storage.loadSettings(store.state)
  store.state.loading = true
  await http.get(`/base-options`).then((res) => {
    if (res.data.success) {
      baseOptions.value = res.data.data
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
  if (!baseOptions.value.includes(store.state.base)) {
    store.state.base = baseOptions.value[0]
  }
  await http.get(`/api-options`).then((res) => {
    if (res.data.success) {
      apiOptions.value = res.data.data
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
  if (!apiOptions.value.includes(store.state.api)) {
    store.state.api = apiOptions.value[0]
  }
  settings.base = store.state.base
  settings.api = store.state.api
  store.state.loading = false
})

const update = () => {
  store.state.base = settings.base
  store.state.api = settings.api
  storage.saveSettings(store.state)
  router.push("/")
}
const cancel = () => {
  router.push("/")
}
</script>

<template>
  <div class="settings">
    <h1 class="title">Settings</h1>
    <el-form class="form" size="large" label-position="top">
      <el-form-item label="Currency Base">
        <el-select v-model="settings.base" placeholder="Currency Base" style="width: 100%;"
          @keyup.enter.native="update">
          <el-option v-for="b in baseOptions" :key="b" :label="b.toUpperCase()" :value="b" />
        </el-select>
      </el-form-item>
      <el-form-item label="API">
        <el-select v-model="settings.api" placeholder="API" style="width: 100%;" @keyup.enter.native="update">
          <el-option label="Currency-api" value="currency" />
          <el-option label="ExchangeRate-API" value="exchange" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="update">Update</el-button>
        <el-button @click="cancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.settings {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

@media (min-width: 420px) {
  .settings {
    justify-content: center;
  }
}

.title,
.divider {
  text-align: center;
}

.form {
  width: 240px;
  padding: 20px 20px 0;
  background-color: #fafbfc;
}
</style>
