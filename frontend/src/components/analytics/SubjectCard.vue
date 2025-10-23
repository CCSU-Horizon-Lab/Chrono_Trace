<template>
  <div class="subject-card">
    <div class="card">
      <div class="header">
        <img v-if="subject?.avatar" :src="subject!.avatar" alt="avatar" />
        <div v-else class="avatar-fallback">{{ subject?.name?.[0] || '?' }}</div>
        <div class="title">
          <div class="name">{{ subject?.name || '未选择对象' }}</div>
          <div class="sub">对象信息</div>
        </div>
      </div>
      <div class="stats" v-if="subject?.stats">
        <div class="stat"><span class="k">消息数</span><span class="v">{{ subject!.stats!.msgCount }}</span></div>
        <div class="stat"><span class="k">平均情绪</span><span class="v">{{ (subject!.stats!.avgScore ?? 0).toFixed(2) }}</span></div>
        <div class="stat"><span class="k">最高日</span><span class="v">{{ subject!.stats!.maxDay || '-' }}</span></div>
        <div class="stat"><span class="k">最低日</span><span class="v">{{ subject!.stats!.minDay || '-' }}</span></div>
      </div>
      <div v-else class="empty">暂无统计</div>
    </div>
  </div>
</template>

<script setup lang="ts">
type SubjectStats = { msgCount: number; avgScore: number; maxDay?: string; minDay?: string }
export type Subject = { id?: string | number; name: string; avatar?: string; stats?: SubjectStats }

defineProps<{ subject?: Subject }>()
</script>

<style scoped>
.card { background: #fff; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); padding: 16px; }
.header { display: flex; align-items: center; gap: 12px; }
.header img { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; }
.avatar-fallback { width: 44px; height: 44px; border-radius: 50%; background: #eef2ff; color: #6366f1; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; }
.title .name { font-size: 16px; font-weight: 700; }
.title .sub { color: #6b7280; font-size: 12px; }
.stats { margin-top: 12px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.stat { background: #f9fafb; border: 1px solid #eef0f3; border-radius: 8px; padding: 8px 10px; display: flex; flex-direction: column; gap: 4px; }
.stat .k { color: #6b7280; font-size: 12px; }
.stat .v { font-weight: 700; }
.empty { color: #6b7280; margin-top: 8px; }
</style>
