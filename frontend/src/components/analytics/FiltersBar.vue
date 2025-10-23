<template>
  <div class="filters-bar">
    <div class="left">
      <div class="subject">
        <span class="avatar" v-if="subjectName?.[0]">{{ subjectName[0] }}</span>
        <div class="info">
          <div class="name" :title="subjectName">{{ subjectName }}</div>
          <div class="hint">分析对象</div>
        </div>
      </div>
    </div>
    <div class="center">
      <div class="dates">
        <input type="date" :value="dates.from" @change="onFrom($event)" />
        <span>—</span>
        <input type="date" :value="dates.to" @change="onTo($event)" />
      </div>
      <div class="quick">
        <button class="btn" @click="quick(7)" :disabled="loading">近7天</button>
        <button class="btn" @click="quick(30)" :disabled="loading">近30天</button>
        <button class="btn" @click="$emit('refresh')" :disabled="loading">刷新</button>
      </div>
    </div>
    <div class="right">
      <button class="btn" :disabled="loading" @click="onExport">导出CSV</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ subjectName: string; dates: { from: string; to: string }; loading?: boolean }>()
const emit = defineEmits<{ (e: 'update:dates', v: { from: string; to: string }): void; (e: 'refresh'): void; (e: 'export'): void }>()

function fmt(d: Date) { return d.toISOString().slice(0, 10) }
function quick(days: number) {
  const to = new Date()
  const from = new Date()
  from.setDate(to.getDate() - (days - 1))
  emit('update:dates', { from: fmt(from), to: fmt(to) })
}
function onFrom(e: Event) { emit('update:dates', { from: (e.target as HTMLInputElement).value, to: props.dates.to }) }
function onTo(e: Event) { emit('update:dates', { from: props.dates.from, to: (e.target as HTMLInputElement).value }) }
function onExport() { emit('export') }
</script>

<style scoped>
.filters-bar {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 12px;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  padding: 12px 16px;
}
.subject { display: flex; align-items: center; gap: 10px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #eef2ff; color: #6366f1; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; }
.info .name { font-weight: 600; }
.info .hint { color: #6b7280; font-size: 12px; }
.center { display: flex; align-items: center; gap: 12px; }
.dates { display: flex; align-items: center; gap: 8px; }
.quick { display: flex; gap: 8px; }
.btn { padding: 6px 10px; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb; cursor: pointer; }
</style>
