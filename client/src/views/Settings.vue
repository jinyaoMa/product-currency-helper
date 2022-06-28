<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

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
    <el-form class="form" size="large" label-position="top" :model="form" @keyup.enter.native="update">
      <el-form-item label="Currency Base">
        <el-input type="text" v-model="store.state.currencyBase" />
      </el-form-item>
      <el-form-item label="Threshold">
        <el-input-number v-model="store.state.threshold" :precision="2" :step="0.1" :min="0" />
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
  background-color: #f1f2f3;
}
</style>
