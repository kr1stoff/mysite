<template>
  <el-form
    ref="ruleFormRef"
    style="max-width: 600px"
    :model="ruleForm"
    :rules="rules"
    label-width="auto"
    class="demo-ruleForm"
    :size="formSize"
    status-icon
  >
    <el-form-item label="芯片号" prop="chipNumber">
      <el-input v-model="ruleForm.chipNumber" placeholder="ChipNumber" />
    </el-form-item>
    <el-form-item label="工作流" prop="workflow">
      <el-select v-model="ruleForm.workflow" filterable placeholder="Workflow">
        <el-option
          v-for="item in selectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="samplesheet" prop="samplesheet">
      <el-upload
        v-model:file-list="fileList"
        class="upload-demo"
        :auto-upload="false"
        multiple
        :limit="1"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        :on-exceed="handleExceed"
      >
        <el-button type="default">点击上传</el-button>
      </el-upload>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        创建
      </el-button>
      <el-button type="warning" @click="resetForm(ruleFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import type {
  ComponentSize,
  FormInstance,
  FormRules,
  UploadProps,
  UploadUserFile,
} from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";

const fileList = ref<UploadUserFile[]>([]);

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
  console.log(file, uploadFiles);
};

const handlePreview: UploadProps["onPreview"] = (uploadFile) => {
  console.log(uploadFile);
};

const handleExceed: UploadProps["onExceed"] = () => {
  ElMessage.warning(`提交文件上限为 1. 已超出限制, 请删除后再上传`);
};

const beforeRemove: UploadProps["beforeRemove"] = (uploadFile) => {
  return ElMessageBox.confirm(`取消上传 ${uploadFile.name} ?`).then(
    () => true,
    () => false
  );
};

// 表单校验
interface RuleForm {
  chipNumber: string;
  workflow: string;
}

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const ruleForm = reactive<RuleForm>({
  chipNumber: "",
  workflow: "",
});

const rules = reactive<FormRules<RuleForm>>({
  workflow: [{ required: true, message: "请选择工作流", trigger: "change" }],
  chipNumber: [
    { required: true, message: "请输入有效的芯片号", trigger: "blur" },
    { min: 10, max: 10, message: "芯片号长度必须为10", trigger: "blur" },
  ],
});

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid) => {
    if (valid) {
      if (fileList.value.length === 0) {
        ElMessage.error("请上传 samplesheet 文件");
        console.log("请上传 samplesheet 文件");
        return;
      }
      const formData = new FormData();
      // 添加表单数据
      formData.append("chipNumber", ruleForm.chipNumber);
      formData.append("workflow", ruleForm.workflow);
      // 添加文件
      formData.append(
        "samplesheet",
        fileList.value[0].raw as Blob,
        fileList.value[0].name
      );
      // 发送请求
      axios
        .post("/api/ngs/workflow", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("提交成功:", response.data);
          ElMessage.success("提交成功");
          // 重置表单和文件列表
          resetForm(formEl);
        })
        .catch((error) => {
          console.error("提交失败:", error);
          ElMessage.error(error.response?.data?.detail || "提交失败，请重试");
        });
    } else {
      ElMessage.error("提交失败，请重试");
    }
  });
};

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
  // 清空文件列表
  fileList.value = [];
};

// 选择工作流
const selectOptions = [
  {
    value: "lvis",
    label: "慢病毒插入位点",
  },
  {
    value: "tcrseq",
    label: "TCR-seq",
  },
];
</script>
