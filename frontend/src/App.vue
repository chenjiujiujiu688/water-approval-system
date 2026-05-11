<template>
  <div class="app-shell">
    <aside class="side-panel">
      <div>
        <p class="side-kicker">Course Project</p>
        <h1>涉水审批智能审核系统</h1>
        <p class="side-copy">
          节点一聚焦项目基础架构、页面交互与服务联通，为后续知识库、MCP 和
          Agent 能力预留清晰扩展接口。
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
