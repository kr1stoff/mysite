<template>
  <el-card
    class="side-nav-container"
    :style="{ width: isCollapse ? '64px' : '200px' }"
  >
    <!-- Menu 菜单 -->
    <el-menu
      class="side-menu"
      active-text-color="#ffd04b"
      background-color="#545c64"
      text-color="#fff"
      default-active="/"
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
        <el-menu-item index="/ngs/workflows">工作流</el-menu-item>
        <el-menu-item index="/ngs/tasks"
          ><template #title>任务列表</template></el-menu-item
        >
      </el-sub-menu>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>设置</template>
      </el-menu-item>
    </el-menu>
    <!-- Collpase 折叠面板 -->
    <div class="collapse-control">
      <el-radio-group v-model="isCollapse">
        <el-radio-button :value="false" v-if="isCollapse"
          ><el-icon><Expand /></el-icon
        ></el-radio-button>
        <el-radio-button :value="true" v-if="!isCollapse"
          ><el-icon><Fold /></el-icon
        ></el-radio-button>
      </el-radio-group>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { ref } from "vue";

import {
  DataAnalysis,
  HomeFilled,
  Expand,
  Fold,
  Setting,
} from "@element-plus/icons-vue";
import { watch } from "vue";

const emit = defineEmits(["update:collapse"]);
const isCollapse = ref(false);

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

// 监听折叠状态变化
watch(isCollapse, (newValue) => {
  emit("update:collapse", newValue);
});
</script>

<style scoped>
/* 容器相关样式 */
.side-nav-container {
  position: relative;
  height: calc(100vh - 60px);  /* 减去底部边距 */
  margin-bottom: 10px;  /* 添加底部边距 */
  width: auto;
  background-color: #545c64;
  padding: 0;
  z-index: 999;
  overflow: visible;
  transform: translateZ(0);
  display: flex;
  flex-direction: column;
}

:deep(.el-card__body) {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: visible;
}

/* 菜单相关样式 */
.side-menu {
  height: calc(100vh - 80px);  /* 调整高度，为底部按钮和边距留出空间 */
  border-right: none;
  z-index: 1;
}

:deep(.el-menu) {
  border-right: none;
  transform-origin: 0 0;
  transform: translateZ(0);
}

:deep(.el-sub-menu .el-sub-menu__title) {
  z-index: 2;
}

:deep(.el-menu--popup) {
  z-index: 3000;
  position: fixed;
  transform: translateZ(0);
  min-width: 200px;
}

/* 折叠控制按钮样式 */
.collapse-control {
  position: relative;  /* 改为相对定位 */
  margin-top: auto;   /* 自动占据顶部空间，实现底部对齐 */
  margin-bottom: 10px;  /* 底部间距 */
  width: 100%;        /* 宽度100% */
  height: 40px;
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;
  background-color: #545c64;
  z-index: 3001;
}

:deep(.el-radio-button__inner) {
  background-color: transparent;
  color: #fff;
  padding: 8px 12px;
  z-index: 3001;
  white-space: nowrap;
  border: none;  /* 移除边框 */
}

:deep(.el-radio-button__inner:hover) {
  color: #ffd04b;
}
</style>
