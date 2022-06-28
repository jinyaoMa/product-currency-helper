<script setup>
import { ref } from 'vue'

const currentDate = ref(new Date())
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
        <el-row>
          <el-col v-for="(o, index) in 8" :key="o" :span="4" :offset="index > 0 ? 1 : 0">
            <el-card :body-style="{ padding: '0px' }" shadow="hover">
              <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
                class="image" />
              <div style="padding: 14px">
                <span>Yummy hamburger</span>
                <div class="bottom">
                  <time class="time">{{ currentDate }}</time>
                  <el-button text class="button">Operating</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
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

@media (min-width: 768px) {
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

.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
</style>
