<template>
  <h2>系统设置</h2>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column label="参数" width="auto">
      <template #default="scope">
        <span>{{ scope.row.argName }}</span>
      </template>
    </el-table-column>
    <el-table-column label="值" width="auto">
      <template #default="scope">
        <span>{{ scope.row.argValue }}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          修改
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from 'vue';

interface SettingArgs {
  argName: string;
  argValue: string;
}

const tableData = ref<SettingArgs[]>([]);

// 获取系统设置
const fetchSettings = async () => {
    try {
        const response = await axios.get("/api/settings");
        tableData.value = response.data;
    } catch (error) {
        console.error(error);
    }
}

const handleEdit = (index: number, row: SettingArgs) => {
  console.log(index, row);
};

// 页面加载时获取数据
fetchSettings();
</script>
