<template>
  <div class="header">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      @select="handleSelect"
      style="display: flex; justify-content: space-between"
    >
      <el-menu-item index="1">金墁利-中心实验室</el-menu-item>
      <el-menu-item index="2">
        <el-avatar :src="circleUrl" />
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
// 顶部导航
import { ref } from "vue";

const activeIndex = ref("1");
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

// 顶部导航 - 头像
import { reactive, toRefs } from "vue";

const state = reactive({
  circleUrl:
    "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
  squareUrl:
    "https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png",
  sizeList: ["small", "", "large"] as const,
});

const { circleUrl } = toRefs(state);
</script>

<style scoped>
.header {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
