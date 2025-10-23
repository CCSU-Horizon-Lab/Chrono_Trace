<template>
  <div class="ct-layout">
    <aside class="ct-sidebar">
      <h2 class="ct-brand">Chrono_Trace</h2>
      <nav class="ct-menu">
        <router-link to="/">首页</router-link>
        <router-link to="/analytics">历史数据</router-link>
        <router-link to="/suggestions">AI建议</router-link>
        <router-link to="/settings">设置</router-link>
      </nav>
    </aside>
    <main class="ct-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
/* 覆盖式兜底，确保侧边栏为左侧垂直布局（即使全局样式未加载也能工作） */
.ct-layout { display: grid; grid-template-columns: 240px 1fr; height: 100vh; }
.ct-sidebar { border-right: 1px solid rgba(0,0,0,0.08); padding: 16px; background: var(--ct-color-primary); color: #fff; }
.ct-brand { margin: 0 0 16px; font-size: 18px; }
.ct-menu { display: flex; flex-direction: column; gap: 8px; }
.ct-menu a { color: #fff; text-decoration: none; padding: 8px 10px; border-radius: 6px; opacity: 0.9; display: block; }
.ct-menu a:hover { opacity: 1; background: rgba(255,255,255,0.08); }
.ct-menu a.router-link-active { background: var(--ct-color-accent); color: #1F2430; }
.ct-content { padding: 16px; overflow: auto; }
</style>
