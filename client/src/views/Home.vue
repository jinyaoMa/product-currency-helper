<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

const bases = ["CAD", "USD"]

const items = reactive([
  {
    id: 1,
    title: "Title 1",
    url: "#",
    img: "https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png",
    price: 99.9,
    base: "USD"
  },
  {
    id: 2,
    title: "Title 2",
    url: "#",
    img: "https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png",
    price: 9999.9,
    base: "USD"
  }
])
items.forEach(item => {
  item.isEdit = false
})

const newItem = reactive({
  title: "",
  url: "",
  img: "",
  price: "",
  base: ""
})

const update = () => {
  router.push("/")
}

const add = () => {
  router.push("/")
}

</script>

<template>
  <div class="home">
    <el-container>
      <el-header class="header">
        <div class="header-appname">Product Currency Helper</div>
        <div class="header-more">
          <el-button-group class="header-more-config">
            <el-button type="primary" size="large" @click="">Settings</el-button>
            <el-button type="primary" size="large" @click="">Access Tokens</el-button>
          </el-button-group>
          <el-button class="header-more-logout" type="danger" size="large" @click="" plain>
            Logout</el-button>
        </div>
      </el-header>
      <el-main>
        <div class="main">
          <el-card class="card" v-for="item in items" :key="item.id" :body-style="{ padding: '0px' }" shadow="hover">
            <div v-if="item.isEdit" class="bottom" style="background-color: transparent">
              <el-form class="form" size="large" :model="newItem">
                <el-form-item>
                  <el-input type="text" v-model="item.title" placeholder="Title"
                    @keyup.enter.native="update(item.id)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="item.url" placeholder="Product URL"
                    @keyup.enter.native="update(item.id)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="text" v-model="item.img" placeholder="Image URL"
                    @keyup.enter.native="update(item.id)" />
                </el-form-item>
                <el-form-item>
                  <el-input type="number" v-model="item.price" placeholder="Price" min="0" step="0.05"
                    @keyup.enter.native="update(item.id)" />
                </el-form-item>
                <el-form-item>
                  <el-select v-model="item.base" placeholder="Currency Base" style="width: 100%;">
                    <el-option v-for="b in bases" :key="b" :label="b" :value="b" />
                  </el-select>
                </el-form-item>
                <el-form-item style="margin-bottom: 0;">
                  <el-button style="width: calc(50% - 0.5em);" type="primary" size="large" @click="update(item.id)">
                    Update
                  </el-button>
                  <el-button style="width: calc(50% - 0.5em); margin-left: 1em;" size="large"
                    @click="item.isEdit = false">Back
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <template v-else>
              <img :src="item.img" class="image" />
              <div class="bottom">
                <div style="font-size: 1.3em; margin-bottom: 0.5em">{{ item.title }}</div>
                <div>{{ store.state.currencyBase }}$ {{ item.price }}</div>
                <div style="font-size: 0.8em">({{ item.base }}$ {{ item.price }})</div>
                <div style="margin-top: 1em">
                  <el-button style="width: 100%;" type="primary" size="large" @click="item.isEdit = true">Edit
                  </el-button>
                </div>
              </div>
            </template>
          </el-card>
          <el-card class="card" :body-style="{ padding: '0px' }" shadow="hover">
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
                    <el-option v-for="b in bases" :key="b" :label="b" :value="b" />
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
  text-shadow: 0.1em 0.1em #999;
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
  margin: 0.5em 0;
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
  height: 382px;
  display: block;
  object-fit: cover;
  object-position: center;
}

.bottom {
  padding: 1em;
  position: absolute;
  bottom: 0;
  background-color: #fff;
  width: 100%;
  box-sizing: border-box;
}
</style>
