<template>
  <section>
    <PageHeader
      kicker="Create"
      title="新建申请"
      description="填写申请人信息、取水用途与附件材料，并提交给 Java 后端。"
    />

    <form class="card form-grid" @submit.prevent="submitApplication">
      <label>
        <span>申请标题</span>
        <input
          v-model="form.title"
          type="text"
          placeholder="例如：某水利工程临时取水申请"
          required
        />
      </label>

      <label>
        <span>申请人姓名</span>
        <input
          v-model="form.applicantName"
          type="text"
          placeholder="请输入申请人姓名"
          required
        />
      </label>

      <label>
        <span>所属单位</span>
        <input
          v-model="form.organizationName"
          type="text"
          placeholder="请输入单位名称"
          required
        />
      </label>

      <label>
        <span>联系电话</span>
        <input v-model="form.contactPhone" type="text" placeholder="请输入联系电话" />
      </label>

      <label>
        <span>电子邮箱</span>
        <input v-model="form.email" type="email" placeholder="请输入电子邮箱" />
      </label>

      <label>
        <span>取水用途</span>
        <input
          v-model="form.waterUsage"
          type="text"
          placeholder="例如：施工降尘、工程调试"
          required
        />
      </label>

      <label>
        <span>取水地点</span>
        <input
          v-model="form.waterLocation"
          type="text"
          placeholder="请输入取水地点"
          required
        />
      </label>

      <label>
        <span>申请期限</span>
        <div class="date-range">
          <input
            v-model="period.startDate"
            type="date"
            aria-label="申请开始日期"
            required
          />
          <span>至</span>
          <input
            v-model="period.endDate"
            type="date"
            aria-label="申请结束日期"
            required
          />
        </div>
      </label>

      <label class="full-width">
        <span>补充说明</span>
        <textarea
          v-model="form.description"
          rows="4"
          placeholder="填写项目背景、材料说明等"
        ></textarea>
      </label>

      <label class="full-width">
        <span>上传附件（支持多个文件）</span>
        <input type="file" multiple @change="handleFiles" />
      </label>

      <div v-if="selectedFiles.length" class="file-list full-width">
        <p>已选择 {{ selectedFiles.length }} 个文件：</p>
        <ul>
          <li v-for="file in selectedFiles" :key="file.name + file.size">{{ file.name }}</li>
        </ul>
      </div>

      <div class="full-width action-row">
        <button class="primary-btn" type="submit" :disabled="submitting">
          {{ submitting ? "提交中..." : "提交申请" }}
        </button>
        <button class="secondary-btn" type="button" @click="resetForm">重置</button>
      </div>

      <p v-if="successMessage" class="success-text full-width">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-text full-width">{{ errorMessage }}</p>
    </form>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";
import { computed } from "vue";
import { useRouter } from "vue-router";
import { createApplication } from "../api/application";
import PageHeader from "../components/PageHeader.vue";

const router = useRouter();

const defaultForm = () => ({
  title: "",
  applicantName: "",
  organizationName: "",
  contactPhone: "",
  email: "",
  waterUsage: "",
  waterLocation: "",
  description: ""
});

const form = reactive(defaultForm());
const period = reactive({
  startDate: "",
  endDate: ""
});
const selectedFiles = ref([]);
const submitting = ref(false);
const successMessage = ref("");
const errorMessage = ref("");

const formattedApplicationPeriod = computed(() => {
  if (!period.startDate || !period.endDate) {
    return "";
  }
  return `${period.startDate} 至 ${period.endDate}`;
});

function handleFiles(event) {
  selectedFiles.value = Array.from(event.target.files || []);
}

function resetForm() {
  Object.assign(form, defaultForm());
  period.startDate = "";
  period.endDate = "";
  selectedFiles.value = [];
  successMessage.value = "";
  errorMessage.value = "";
}

async function submitApplication() {
  submitting.value = true;
  successMessage.value = "";
  errorMessage.value = "";

  if (period.endDate < period.startDate) {
    errorMessage.value = "申请期限填写有误：结束日期不能早于开始日期。";
    submitting.value = false;
    return;
  }

  const payload = new FormData();
  Object.entries(form).forEach(([key, value]) => {
    payload.append(key, value);
  });
  payload.append("applicationPeriod", formattedApplicationPeriod.value);
  selectedFiles.value.forEach((file) => payload.append("files", file));

  try {
    const { data } = await createApplication(payload);
    resetForm();
    successMessage.value = `申请提交成功，申请编号：${data.id}`;
    router.push(`/review?id=${data.id}`);
  } catch (error) {
    errorMessage.value = "申请提交失败，请确认后端接口与跨域配置正常。";
  } finally {
    submitting.value = false;
  }
}
</script>
