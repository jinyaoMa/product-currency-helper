<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const accessTokens = [{
  id: 1,
  token: "abcabcab",
  permission: "basic:1,manipulation:1,advanced:0",
  active: true
}]

const newPerm = reactive({
  basic: true,
  manipulation: false,
  advanced: false
})

const handleDisable = () => {
  router.push("/")
}
const handleEnable = () => {
  router.push("/")
}
const handleNew = () => {
  router.push("/")
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
      <el-table-column prop="token" label="Access Token" min-width="130" />
      <el-table-column prop="permission" label="Permission" min-width="270" />
      <el-table-column fixed="right" label="Operations" width="120">
        <template #default="scope">
          <el-button v-if="scope.row.active" link type="danger" @click="handleDisable">Disable</el-button>
          <el-button v-else link type="success" @click="handleEnable">Enable</el-button>
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
