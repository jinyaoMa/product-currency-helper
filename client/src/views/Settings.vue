<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const bases = ["CAD", "USD"]

const update = () => {
  router.push("/")
}
const cancel = () => {
  router.push("/")
}
</script>

<template>
  <div class="settings">
    <h1 class="title">Settings</h1>
    <el-form class="form" size="large" label-position="top" :model="form">
      <el-form-item label="Currency Base">
        <el-select v-model="store.state.currencyBase" placeholder="Currency Base" style="width: 100%;"
          @keyup.enter.native="update">
          <el-option v-for="b in bases" :key="b" :label="b" :value="b" />
        </el-select>
      </el-form-item>
      <el-form-item label="API">
        <el-select v-model="store.state.api" placeholder="API" style="width: 100%;" @keyup.enter.native="update">
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
