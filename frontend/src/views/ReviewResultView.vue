<template>
  <section>
    <PageHeader
      kicker="Review"
      title="初审结果"
      description="当前节点一仅展示模拟初审结果，后续节点将替换为真实 AI 审核结果。"
    />

    <div class="toolbar">
      <label class="inline-input">
        <span>申请 ID</span>
        <input v-model="applicationId" type="number" min="1" placeholder="请输入申请 ID" />
      </label>
      <button class="primary-btn" @click="loadReview">获取初审结果</button>
    </div>

    <div class="card result-grid" v-if="result">
      <div>
        <p class="label-text">审核状态</p>
        <h3>{{ result.reviewStatus }}</h3>
      </div>
      <div>
        <p class="label-text">风险等级</p>
        <h3>{{ result.riskLevel }}</h3>
      </div>
      <div class="full-width">
        <p class="label-text">审核摘要</p>
        <p>{{ result.summary }}</p>
      </div>
      <div class="full-width">
        <p class="label-text">建议项</p>
        <p>{{ result.suggestions }}</p>
      </div>
      <div>
        <p class="label-text">申请标题</p>
        <p>{{ result.applicationTitle }}</p>
      </div>
      <div>
        <p class="label-text">生成时间</p>
        <p>{{ result.reviewedAt }}</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { fetchReviewResult } from "../api/application";
import PageHeader from "../components/PageHeader.vue";

const route = useRoute();
const applicationId = ref(route.query.id || "1");
const result = ref(null);
const errorMessage = ref("");

async function loadReview() {
  errorMessage.value = "";
  result.value = null;

  if (!applicationId.value) {
    errorMessage.value = "请先输入申请 ID。";
    return;
  }

  try {
    const { data } = await fetchReviewResult(applicationId.value);
    result.value = data;
  } catch (error) {
    errorMessage.value = "初审结果获取失败，请确认申请已经存在。";
  }
}

onMounted(loadReview);
</script>
