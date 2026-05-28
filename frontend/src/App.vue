<template>
  <div class="app-shell">
    <aside class="side-panel">
      <div>
        <p class="side-kicker">Course Project</p>
        <h1>涉水审批智能审核系统</h1>
        <p class="side-copy">
          面向取水许可申请材料，提供申请提交、附件管理、知识库检索与
          AI 初审辅助，帮助快速发现材料缺失和填报风险。
        </p>
      </div>

      <nav class="nav-links">
        <RouterLink to="/">申请列表</RouterLink>
        <RouterLink to="/applications/new">新建申请</RouterLink>
        <RouterLink to="/review">初审结果</RouterLink>
      </nav>
    </aside>

    <main class="main-panel">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>
