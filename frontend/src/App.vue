<template>
  <div class="layout">
    <aside class="sidebar">
      <h2 class="brand">Chrono_Trace</h2>
      <nav class="menu">
        <router-link to="/">首页</router-link>
        <router-link to="/analytics">历史数据</router-link>
        <router-link to="/suggestions">AI建议</router-link>
        <router-link to="/settings">设置</router-link>
      </nav>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
  :root { color-scheme: light dark; }
  .layout { display: grid; grid-template-columns: 240px 1fr; height: 100vh; font-family: system-ui, -apple-system, Segoe UI, Roboto, 'Helvetica Neue', Arial; }
  .sidebar { border-right: 1px solid #eee; padding: 16px; }
  .brand { margin: 0 0 16px; font-size: 18px; }
  .menu { display: flex; flex-direction: column; gap: 8px; }
  .menu a { color: inherit; text-decoration: none; padding: 8px 10px; border-radius: 6px; }
  .menu a.router-link-active { background: #f2f3f5; }
  .content { padding: 16px; overflow: auto; }
</style>
