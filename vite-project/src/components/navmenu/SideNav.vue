<template>
  <el-card class="side-nav-container">
    <!-- Collpase 折叠面板 -->
    <div class="collapse-control">
      <el-radio-group v-model="isCollapse" style="margin-bottom: 10px">
        <el-radio-button :value="false" v-if="isCollapse"
          ><el-icon><CaretRight /></el-icon
        ></el-radio-button>
        <el-radio-button :value="true" v-if="!isCollapse"
          ><el-icon><CaretLeft /></el-icon
        ></el-radio-button>
      </el-radio-group>
    </div>
    <!-- Menu 菜单 -->
    <el-menu
      default-active="/"
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      @open="handleOpen"
      @close="handleClose"
      router
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        <template #title>主页</template>
      </el-menu-item>
      <el-sub-menu index="/ngs">
        <template #title>
          <el-icon><DataAnalysis /></el-icon>
          <span>NGS 流程自动化</span>
        </template>
        <el-menu-item index="/ngs/samplesheet"
          >Illumina - samlesheet</el-menu-item
        >
        <el-menu-item index="/ngs/lvis">慢病毒插入位点</el-menu-item>
        <el-menu-item index="/ngs/tcrseq">TCR-seq</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>设置</template>
      </el-menu-item>
    </el-menu>
  </el-card>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import {
  DataAnalysis,
  HomeFilled,
  CaretRight,
  CaretLeft,
} from "@element-plus/icons-vue";
import { Setting } from "@element-plus/icons-vue";

const isCollapse = ref(false);

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}

.el-menu-vertical-demo {
  height: 100%;
}

.side-nav-container {
  position: relative;
}

.collapse-control {
  position: absolute;
  top: 5px;
  right: 5px;
  z-index: 1;
}
</style>
