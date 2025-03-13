<template>
  <div class="common-layout">
    <TopNav />
    <el-container>
      <el-aside :width="sideWidth">
        <SideNav @update:collapse="handleCollapse" />
      </el-aside>
      <el-main><slot></slot></el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import TopNav from "./TopNav.vue";
import SideNav from "./SideNav.vue";

const sideWidth = ref("200px");

const handleCollapse = (isCollapse: boolean) => {
  sideWidth.value = isCollapse ? "64px" : "200px";
};
</script>

<style scoped></style>
