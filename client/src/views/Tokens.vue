<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { http } from '../http'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const accessTokens = ref([])

const newPerm = reactive({
  basic: true,
  manipulation: false,
  advanced: false
})

onMounted(() => {
  store.state.loading = true
  http.get(`/token/list`).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      accessTokens.value = res.data.data
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    store.state.loading = false
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
})

const handleDisable = (token) => {
  store.state.loading = true
  http.post(`/token/${token.id}/deactivate`).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      token.active = false
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    store.state.loading = false
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
}
const handleEnable = (token) => {
  store.state.loading = true
  http.post(`/token/${token.id}/activate`).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      token.active = true
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    store.state.loading = false
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
}
const handleNew = () => {
  store.state.loading = true
  let permissionString = "b"
  if (newPerm.manipulation) {
    permissionString += "m"
  }
  if (newPerm.advanced) {
    permissionString += "a"
  }
  http.put(`/token/${permissionString}`).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      accessTokens.value.push(res.data.data)
    } else {
      router.push("/login")
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
  }).catch(() => {
    store.state.loading = false
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
}
const handleBack = () => {
  router.push("/")
}
</script>

<template>
  <div class="tokens">
    <h1 class="title">Access Tokens</h1>
    <el-table class="table" :data="accessTokens" size="large">
      <el-table-column prop="id" label="ID" width="50" />
      <el-table-column prop="access_token" label="Access Token" min-width="180">
        <template #default="scope">
          <span style="margin-right:1em">{{ scope.row.access_token }}</span>
          <el-tag :type="scope.row.active == 1 ? '' : 'info'" disable-transitions>
            {{ scope.row.active == 1 ? "Active" : "Inactive" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="permission" label="Permission" min-width="270" />
      <el-table-column fixed="right" label="Operations" width="120">
        <template #default="scope">
          <el-button v-if="scope.row.active" size="small" type="danger" @click="handleDisable(scope.row)"
            style="width:100%">
            Disable
          </el-button>
          <el-button v-else size="small" type="success" @click="handleEnable(scope.row)" style="width:100%">
            Enable
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-form class="form" size="large" label-position="top">
      <el-form-item label="New Token Permission">
        <el-checkbox v-model="newPerm.basic" label="Basic" disabled />
        <el-checkbox v-model="newPerm.manipulation" label="Manipulation" />
        <el-checkbox v-model="newPerm.advanced" label="Advanced" />
      </el-form-item>
      <el-form-item>
        <el-button size="large" @click="handleNew" type="primary">New</el-button>
        <el-button size="large" @click="handleBack">Back</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.tokens {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

@media (min-width: 420px) {
  .tokens {
    justify-content: center;
  }
}

.title,
.divider {
  text-align: center;
}

.table {
  max-width: 800px;
  margin-bottom: 1.3em;
}

.form {
  margin-top: 1.3em;
  width: 240px;
  padding: 20px 20px 0;
  background-color: #fafbfc;
}
</style>
