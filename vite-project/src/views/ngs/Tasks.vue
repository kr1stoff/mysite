<template>
  <el-table :data="filterTableData" style="width: 100%">
    <el-table-column
      label="任务编号"
      prop="task_number"
      min-width="200"
      show-overflow-tooltip
    />
    <el-table-column
      label="芯片号"
      prop="chip_number"
      min-width="120"
      show-overflow-tooltip
    />
    <el-table-column
      label="工作流"
      prop="workflow"
      min-width="100"
      show-overflow-tooltip
    />
    <el-table-column
      label="创建时间"
      prop="created_at"
      min-width="150"
      show-overflow-tooltip
    />
    <el-table-column
      label="完成时间"
      prop="completed_at"
      min-width="150"
      show-overflow-tooltip
    />
    <el-table-column label="BCL" prop="bcl_status" min-width="90" show-overflow-tooltip>
      <template #default="scope">
        <el-tag :type="getStatusType(scope.row.bcl_status)">
          {{ getStatusText(scope.row.bcl_status) }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="FASTQ" prop="fastq_status" min-width="90" show-overflow-tooltip>
      <template #default="scope">
        <el-tag :type="getStatusType(scope.row.fastq_status)">
          {{ getStatusText(scope.row.fastq_status) }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="分析" prop="analysis_status" min-width="90" show-overflow-tooltip>
      <template #default="scope">
        <el-tag :type="getStatusType(scope.row.analysis_status)">
          {{ getStatusText(scope.row.analysis_status) }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" min-width="150" show-overflow-tooltip>
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          重启
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
    <el-table-column width="130" show-overflow-tooltip>
      <template #header>
        <el-input v-model="search" autosize placeholder="键入进行搜索" />
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { ElMessage } from "element-plus";
import { computed, ref, onMounted } from "vue";
import axios from "axios";

interface Task {
  id: number;
  task_number: string;
  chip_number: string;
  workflow: string;
  created_at: string;
  completed_at: string;
  bcl_status: string;
  fastq_status: string;
  analysis_status: string;
}

const search = ref("");
const tableData = ref<Task[]>([]);

const filterTableData = computed(() =>
  tableData.value.filter(
    (data) =>
      !search.value ||
      data.task_number.toLowerCase().includes(search.value.toLowerCase()) ||
      data.chip_number.toLowerCase().includes(search.value.toLowerCase()) ||
      data.workflow.toLowerCase().includes(search.value.toLowerCase())
  )
);

const fetchTasks = async () => {
  try {
    const response = await axios.get("/api/ngs/tasks");
    // 确保 response.data 是一个数组
    tableData.value = Array.isArray(response.data) ? response.data : [];
    console.log("获取的数据:", tableData.value); // 调试用
  } catch (error) {
    console.error("获取任务列表失败:", error);
    ElMessage.error(`获取任务列表失败: ${error}`);
  }
};

onMounted(() => {
  fetchTasks();
});

// 获取转换状态
const getStatusText = (status: string) => {
  const statusMap: { [key: string]: string } = {
    "0": "未开始",
    "1": "进行中",
    "2": "已完成",
    "3": "异常",
  };
  return statusMap[status] || "未知";
};

const getStatusType = (status: string) => {
  const statusMap: { [key: string]: string } = {
    "0": "info",
    "1": "warning",
    "2": "success",
    "3": "error",
  };
  return statusMap[status] || "";
};

// 编辑和删除
const handleEdit = (index: number, row: Task) => {
  console.log(index, row);
  axios.put(`/api/ngs/tasks/${row.id}`).then((response) => {
    console.log("重启成功:", response.data);
    ElMessage.success("重启成功");
    fetchTasks();
  }).catch((error) => {
    console.error("重启失败:", error);
    ElMessage.error(error.response?.data?.detail || "重启失败，请重试");
  });
};

const handleDelete = (index: number, row: Task) => {
  console.log(index, row);
  axios.delete(`/api/ngs/tasks/${row.id}`).then((response) => {
    console.log("删除成功:", response.data);
    ElMessage.success("删除成功");
    fetchTasks();
  }).catch((error) => {
    console.error("删除失败:", error);
    ElMessage.error(error.response?.data?.detail || "删除失败，请重试");
  });
};
</script>
