<template>
  <h2>Illumina samplesheet</h2>
  <div class="button-group">
    <el-button type="default" @click="downloadTemplate">下载模板</el-button>

    <!-- 上传文件 -->
    <el-upload
      v-model:file-list="fileList"
      class="upload-demo"
      :auto-upload="false"
      :on-change="handleFileChange"
      multiple
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      :limit="1"
      :on-exceed="handleExceed"
    >
      <el-button type="primary">点击上传</el-button>
      <template #tip>
        <div class="el-upload__tip">
          注意:
          <br />
          1. 文件需要小于500KB, 仅支持 Excel 格式
          <br />
          2. 请确保文件中包含以下列: Sample_ID, index, index2 (如有)
          <br />
          3. Sample_ID 必须唯一, 不包含特殊字符
          <br />
          4. index+index2, 必须唯一. 若仅有 index, 则 index 必须唯一
          <br />
          5. <u>不可更改模板中的列名</u>
        </div>
      </template>
    </el-upload>

    <!-- 下载生成的 samplesheet -->
    <el-button
      v-if="downloadInfo.show"
      type="success"
      @click="downloadGeneratedFile"
    >
      结果下载
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { UploadProps, UploadUserFile } from "element-plus";
import axios from "axios"; // 导入axios库

const fileList = ref<UploadUserFile[]>([]);
const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
  console.log(file, uploadFiles);
};
const handlePreview: UploadProps["onPreview"] = (uploadFile) => {
  console.log(uploadFile);
};
const handleExceed: UploadProps["onExceed"] = (files, uploadFiles) => {
  ElMessage.warning(
    `The limit is 1, you selected ${files.length} files this time, add up to ${
      files.length + uploadFiles.length
    } totally`
  );
};
const beforeRemove: UploadProps["beforeRemove"] = (uploadFile) => {
  return ElMessageBox.confirm(
    `Cancel the transfer of ${uploadFile.name} ?`
  ).then(
    () => true,
    () => false
  );
};
// 添加文件变化处理函数
const handleFileChange = (file: UploadUserFile) => {
  // 这里可以添加文件验证逻辑
  console.log("文件已选择:", file);
  // 创建一个 FormData 对象
  const formData = new FormData();
  // 确保 file.raw 是 Blob 类型，并提供文件名
  if (file.raw instanceof Blob) {
    formData.append("file", file.raw, file.name);
  } else {
    console.error("文件不是有效的 Blob 类型");
  }
  // 发送 POST 请求
  axios
    .post("/api/ngs/samplesheet", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      console.log("文件上传成功:", response.data);
      // 更新下载信息
      downloadInfo.value = {
        show: true,
        filename: response.data.filename,
        taskId: response.data.task_id,
      };
      ElMessage.success("samplesheet 生成成功");
    })
    .catch((error) => {
      console.error("文件上传失败:", error);
      ElMessage.error(`samplesheet 生成失败, ${error.response.data.detail}`);
    });
};

// 下载模板
const downloadTemplate = () => {
  const link = document.createElement("a");
  link.href = "/api/template/samplesheet-template.xlsx"; // 模板文件路径
  link.download = "samplesheet-template.xlsx";
  link.click();
};

// 添加下载文件的状态管理
const downloadInfo = ref({
  show: false,
  filename: "",
  taskId: "",
});
// 添加下载生成文件的方法
const downloadGeneratedFile = () => {
  const link = document.createElement("a");
  link.href = `/api/ngs/samplesheet/${downloadInfo.value.taskId}/${downloadInfo.value.filename}`;
  link.download = downloadInfo.value.filename;
  link.click();
};
</script>

<style scoped>
.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.button-group .el-button {
  width: auto;
  align-self: flex-start;
}
</style>
