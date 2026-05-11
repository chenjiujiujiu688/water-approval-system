<template>
  <section>
    <PageHeader
      kicker="Overview"
      title="申请列表"
      description="查看已提交的涉水审批申请，并快速进入初审结果页面。"
    />

    <div class="toolbar">
      <button class="primary-btn" @click="$router.push('/applications/new')">新建申请</button>
      <button class="secondary-btn" @click="loadApplications">刷新列表</button>
    </div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>申请标题</th>
            <th>申请人</th>
            <th>单位</th>
            <th>取水地点</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7">正在加载申请列表...</td>
          </tr>
          <tr v-else-if="applications.length === 0">
            <td colspan="7">暂无申请数据，请先创建申请。</td>
          </tr>
          <tr v-for="item in applications" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.applicantName }}</td>
            <td>{{ item.organizationName }}</td>
            <td>{{ item.waterLocation }}</td>
            <td>
              <span class="status-tag">{{ item.status }}</span>
            </td>
            <td>
              <button class="table-link" @click="viewReview(item.id)">查看初审</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchApplications } from "../api/application";
import PageHeader from "../components/PageHeader.vue";

const router = useRouter();
const applications = ref([]);
const loading = ref(false);
const errorMessage = ref("");

async function loadApplications() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const { data } = await fetchApplications();
    applications.value = data;
  } catch (error) {
    errorMessage.value = "申请列表加载失败，请确认后端服务已经启动。";
  } finally {
    loading.value = false;
  }
}

function viewReview(id) {
  router.push({ path: "/review", query: { id } });
}

onMounted(loadApplications);
</script>
