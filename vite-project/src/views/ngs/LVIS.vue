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
      <el-input v-model="ruleForm.chipNumber" />
    </el-form-item>
    <el-form-item label="samplesheet" prop="samplesheet">
      <!-- <el-input v-model="ruleForm.samplesheet" /> -->
      <el-upload
        v-model:file-list="fileList"
        class="upload-demo"
        :auto-upload="false"
        multiple
        :limit="1"
      >
        <el-button type="default">点击上传</el-button>
      </el-upload>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        创建
      </el-button>
      <el-button @click="resetForm(ruleFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import type { ComponentSize, FormInstance, FormRules } from "element-plus";
import type { UploadUserFile } from "element-plus";

const fileList = ref<UploadUserFile[]>([]);

interface RuleForm {
  chipNumber: string;
}

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const ruleForm = reactive<RuleForm>({
  chipNumber: "AHKM52BGXW",
});

const rules = reactive<FormRules<RuleForm>>({
  chipNumber: [
    { required: true, message: "请输入有效的芯片号", trigger: "blur" },
    { min: 10, max: 10, message: "芯片号长度必须为10", trigger: "blur" },
  ],
});

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log("submit!");
    } else {
      console.log("error submit!", fields);
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};
</script>
