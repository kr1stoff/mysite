<template>
  <h2>系统设置</h2>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column label="参数" width="auto">
      <template #default="scope">
        <span>{{ scope.row.arg_name }}</span>
      </template>
    </el-table-column>
    <el-table-column label="值" width="auto">
      <template #default="scope">
        <span>{{ scope.row.arg_value }}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.row)">
          修改
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";

interface SettingArgs {
  arg_name: string;
  arg_value: string;
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
};

const handleEdit = (row: SettingArgs) => {
  ElMessageBox.prompt("请输入新的值", "修改参数", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    inputValue: row.arg_value,
    inputErrorMessage: "值不能为空",
    customClass: "custom-message-box",
  })
    .then(({ value }) => {
      row.arg_value = value;
      console.log("修改成功", value)
      // 在这里可以发送更新请求到服务器
      axios.post('/api/settings', { arg_name: row.arg_name, arg_value: value })
        .then(response => {
          console.log('更新成功', response);
          ElMessage({
            type: "success",
            message: "更新成功!",
          });
        })
        .catch(error => {
          console.error('更新失败', error);
          ElMessage({
            type: "error",
            message: `更新失败! ${error.response?.data?.detail}` || "更新失败",
          });
          fetchSettings();
        });
    })
    .catch(error => {
      console.error('取消修改', error);
      ElMessage({
        type: "info",
        message: "取消修改",
      });
    });
};

// 页面加载时获取数据
fetchSettings();
</script>
