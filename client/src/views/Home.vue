<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { http } from '../http'
import { ElMessage } from 'element-plus'
import { storage } from '../utils'

const route = useRoute()
const router = useRouter()
const store = useStore()

const baseOptions = ref([])
const apiOptions = ref([])
const rates = ref({})

const items = ref([])

const newItem = reactive({
  title: "",
  url: "",
  img: "",
  price: "",
  base: ""
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
  await http.get(`/service/${store.state.api}/base/${store.state.base}`).then((res) => {
    if (res.data.success) {
      rates.value = res.data.data.to
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
  await http.get(`/product/list`).then((res) => {
    if (res.data.success) {
      res.data.data.forEach(item => {
        item.isEdit = false
      })
      items.value = res.data.data.filter((item) => item.active == 1)
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
  store.state.loading = false
  storage.saveSettings(store.state)
})

const logout = () => {
  store.state.loading = true
  http.get(`/logout`).then((res) => {
    store.state.loading = false
    if (!res.data.success) {
      ElMessage({
        message: "You have not logged in",
        type: "error"
      })
    }
    router.push("/login")
  }).catch(() => {
    store.state.loading = false
    router.push("/login")
    ElMessage({
      message: "Oops, server is down",
      type: "error"
    })
  })
}

const update = (item) => {
  if (item.title == "" ||
    !item.url.startsWith("http") ||
    !item.img.startsWith("http") ||
    item.price == "" ||
    item.base == "") {
    ElMessage({
      message: "Some values are not good to update",
      type: "error"
    })
    return
  }
  store.state.loading = true
  http.post(`/product`, item).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      const i = res.data.data
      item.title = i.title
      item.url = i.url
      item.img = i.img
      item.price = i.price
      item.base = i.base
      item.isEdit = false
      ElMessage({
        message: `Product with ID ${item.id} updated`,
        type: "success"
      })
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

const remove = (item) => {
  store.state.loading = true
  http.delete(`/product/${item.id}`).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      items.value.splice(items.value.indexOf(item), 1)
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

const add = () => {
  if (newItem.title == "" ||
    !newItem.url.startsWith("http") ||
    !newItem.img.startsWith("http") ||
    newItem.price == "" ||
    newItem.base == "") {
    ElMessage({
      message: "Some values are not good to add",
      type: "error"
    })
    return
  }
  store.state.loading = true
  http.put(`/product`, newItem).then((res) => {
    store.state.loading = false
    if (res.data.success) {
      items.value.push(res.data.data)
      newItem.title = ""
      newItem.url = ""
      newItem.img = ""
      newItem.price = ""
      newItem.base = ""
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

</script>

<template>
  <div class="home">
    <el-container>
      <el-header class="header" style="box-shadow: 0 0 1px #666">
        <div class="header-appname">Product Currency Helper</div>
        <div class="header-more">
          <el-button-group class="header-more-config">
            <el-button type="primary" size="large" @click="router.push('/settings')">Settings</el-button>
            <el-button v-if="route.params.permission.advanced" type="primary" size="large"
              @click="router.push('/tokens')">Access Tokens</el-button>
          </el-button-group>
          <el-button class="header-more-logout" type="danger" size="large" @click="logout" plain>
            Logout</el-button>
        </div>
      </el-header>
      <el-main>
        <div class="main">
          <el-card class="card" v-for="item in items" :key="item.id" :body-style="{ padding: '0px' }" shadow="hover">
            <div v-if="item.isEdit" class="bottom" style="background-color: transparent">
              <el-form class="form" size="large">
                <el-form-item>
                  <el-input type="text" v-model="item.title" placeholder="Title" @keyup.enter.native="update(item)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="item.url" placeholder="Product URL"
                    @keyup.enter.native="update(item)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="item.img" placeholder="Image URL" @keyup.enter.native="update(item)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="number" v-model="item.price" placeholder="Price" min="0" step="0.05"
                    @keyup.enter.native="update(item)" />
                </el-form-item>
                <el-form-item>
                  <el-select v-model="item.base" placeholder="Currency Base" style="width: 100%;">
                    <el-option v-for="b in baseOptions" :key="b" :label="b.toUpperCase()" :value="b" />
                  </el-select>
                </el-form-item>
                <el-form-item style="margin-bottom: 0;">
                  <el-button style="width: calc(50% - 0.5em);" type="primary" size="large" @click="update(item)">
                    Update
                  </el-button>
                  <el-button style="width: calc(50% - 0.5em); margin-left: 1em;" size="large"
                    @click="item.isEdit = false">Back
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <template v-else>
              <div v-if="route.params.permission.manipulation" class="button-delete" @click="remove(item)"></div>
              <img :src="item.img" class="image" />
              <div class="bottom">
                <a class="title-link" :href="item.url" target="_blank">{{ item.title }}</a>
                <div v-if="store.state.base == item.base">{{ store.state.base.toUpperCase() }}$ {{
                    item.price.toFixed(2)
                }}</div>
                <div v-else>{{ store.state.base.toUpperCase() }}$ {{ (item.price / rates[item.base]).toFixed(2) }}</div>
                <div style="font-size: 0.8em">({{ item.base.toUpperCase() }}$ {{ item.price.toFixed(2) }})</div>
                <div v-if="route.params.permission.manipulation" style="margin-top: 1em">
                  <el-button style="width: 100%;" type="primary" size="large" @click="item.isEdit = true">Edit
                  </el-button>
                </div>
              </div>
            </template>
          </el-card>
          <el-card v-if="route.params.permission.manipulation" class="card" :body-style="{ padding: '0px' }"
            shadow="hover">
            <div class="bottom">
              <el-form class="form" size="large" :model="newItem">
                <el-form-item>
                  <el-input type="text" v-model="newItem.title" placeholder="Title" @keyup.enter.native="add" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="newItem.url" placeholder="Product URL" @keyup.enter.native="add" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="newItem.img" placeholder="Image URL" @keyup.enter.native="add" />
                </el-form-item>
                <el-form-item>
                  <el-input type="number" v-model="newItem.price" placeholder="Price" min="0" step="0.05"
                    @keyup.enter.native="add" />
                </el-form-item>
                <el-form-item>
                  <el-select v-model="newItem.base" placeholder="Currency Base" style="width: 100%;">
                    <el-option v-for="b in baseOptions" :key="b" :label="b.toUpperCase()" :value="b" />
                  </el-select>
                </el-form-item>
                <el-form-item style="margin-bottom: 0;">
                  <el-button style="width: 100%;" type="success" size="large" @click="add">Add
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: auto;
  min-height: 5em;
}

@media (min-width: 800px) {
  .header {
    flex-direction: row;
  }

  .header-more-config {
    margin: 0 1em;
  }
}

.header-appname {
  font-size: 2em;
  font-weight: bold;
  margin: 0.5em 0;
  text-align: center;
  color: #337ecc;
  text-shadow: 2px 2px #7ebeff;
}

.header-more {
  text-align: center;
}

@media (min-width: 320px) {
  .header-more-config {
    margin: 0 1em;
  }
}

.header-more-logout {
  margin: 14px 0;
}

.main {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.card {
  box-sizing: border-box;
  margin: 0 20px 20px 0;
  position: relative;
  height: 384px;
  transition: none;
  overflow: visible;
}

@media (min-width: 1414px) {
  .card {
    width: calc((100% - 4 * 20px) / 5);
  }

  .card:nth-child(5n) {
    margin-right: 0;
  }
}

@media (min-width: 1166px) and (max-width: 1414px) {
  .card {
    width: calc((100% - 3 * 20px) / 4);
  }

  .card:nth-child(4n) {
    margin-right: 0;
  }
}

@media (min-width: 768px) and (max-width: 1166px) {
  .card {
    width: calc((100% - 2 * 20px) / 3);
  }

  .card:nth-child(3n) {
    margin-right: 0;
  }
}

@media (min-width: 480px) and (max-width: 768px) {
  .card {
    width: calc((100% - 1 * 20px) / 2);
  }

  .card:nth-child(2n) {
    margin-right: 0;
  }
}

@media (max-width: 480px) {
  .card {
    width: 100%;
    margin-right: 0;
  }
}

.image {
  width: 100%;
  height: 280px;
  display: block;
  object-fit: cover;
  object-position: top center;
  background-color: #f1f2f3;
}

.bottom {
  padding: 1em;
  position: absolute;
  bottom: 0;
  background-color: #fff;
  width: 100%;
  box-sizing: border-box;
}

.title-link {
  display: block;
  font-size: 1.3em;
  margin-bottom: 0.5em;
  text-decoration: none;
  color: #409eff;
  word-break: break-all;
}

.title-link:hover {
  text-decoration: underline;
}

.button-delete {
  position: absolute;
  right: -0.8em;
  top: -0.8em;
  width: 3em;
  height: 3em;
  border-radius: 50%;
  background-color: #f56c6c;
  opacity: 0;
  pointer-events: none;
  transition: all 0.2s;
  cursor: pointer;
}

.button-delete:hover {
  background-color: #f89898;
}

.button-delete:before,
.button-delete:after {
  content: "";
  position: absolute;
  top: 25%;
  left: calc(50% - 2px);
  height: 1.2em;
  transform-origin: 50% 50%;
  border: 2px solid #fff;
}

.button-delete:before {
  transform: rotate(45deg);
}

.button-delete:after {
  transform: rotate(-45deg);
}

.card:hover .button-delete {
  opacity: 1;
  pointer-events: all;
}
</style>
