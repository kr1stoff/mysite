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
        <el-menu-item index="/ngs/lvis">慢病毒插入位点</el-menu-item>
        <el-menu-item index="/ngs/tcrseq">TCR-seq</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/tasks">
        <el-icon><List /></el-icon>
        <template #title>任务列表</template>
      </el-menu-item>
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
  List,
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
.side-menu {
  height: calc(100vh - 60px); /* 调整高度，留出底部空间 */
  border-right: none;
}

.side-nav-container {
  position: relative;
  height: 100vh;
  background-color: #545c64;
  padding: 0;
}

:deep(.el-card__body) {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.collapse-control {
  position: fixed; /* 改为固定定位 */
  bottom: 10px;
  left: 20px;
  z-index: 100; /* 提高层级 */
  height: 40px;
  display: flex;
  align-items: center;
  background-color: #545c64; /* 确保背景色一致 */
}

:deep(.el-radio-button__inner) {
  background-color: transparent;
  /* border: none; */
  color: #fff;
  padding: 8px 12px; /* 增加按钮可点击区域 */
}

:deep(.el-radio-button__inner:hover) {
  color: #ffd04b;
}
</style>
