<template>
  <div class="layout-container">
    <!-- 顶部导航 -->
    <TopNav />

    <!-- 主要内容区 -->
    <div class="main-container">
      <!-- 侧边栏 -->
      <SideNav />

      <!-- 右侧内容区 -->
      <div class="content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import TopNav from "./TopNav.vue";
import SideNav from "./SideNav.vue";
</script>

<style>
/* 全局样式 */
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100vh;
}
</style>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
}

.main-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  background-color: #f0f2f5;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #fff;
  margin: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
}
</style>
