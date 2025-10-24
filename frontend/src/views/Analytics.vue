<template>
  <section class="analytics-page">
    <header class="page-title">
      <h1>历史数据</h1>
    </header>

    <FiltersBar
      :subject-name="subject?.name || '未选择对象'"
      :dates="dates"
      :loading="loading"
      @update:dates="onDatesChange"
      @refresh="loadAnalysis"
    />

    <div class="grid">
      <div class="col">
        <div class="card">
          <header class="card-header">
            <h2>历史情绪曲线</h2>
          </header>
          <div class="card-body">
            <div v-if="loading" class="skeleton">加载中…</div>
            <div v-else-if="error" class="error">
              <span>{{ error }}</span>
              <button class="btn" @click="loadAnalysis">重试</button>
            </div>
            <div v-else>
              <EmotionLineChart :timeseries="analysis.timeseries" />
            </div>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <header class="card-header">
            <h2>聊天词云</h2>
          </header>
          <div class="card-body">
            <div v-if="loading" class="skeleton">加载中…</div>
            <div v-else-if="error" class="error">
              <span>{{ error }}</span>
              <button class="btn" @click="loadAnalysis">重试</button>
            </div>
            <div v-else>
              <WordCloud :words="analysis.wordcloud" @select="onWordSelect" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom">
      <SubjectCard :subject="subject" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'
import FiltersBar from '@/components/analytics/FiltersBar.vue'
import SubjectCard from '@/components/analytics/SubjectCard.vue'
import EmotionLineChart from '@/components/charts/EmotionLineChart.vue'
import WordCloud from '@/components/charts/WordCloud.vue'

type TimeseriesPoint = { ts: string; score: number; positive?: number; negative?: number }
type SubjectStats = { msgCount: number; avgScore: number; maxDay?: string; minDay?: string }
type Subject = { id?: string | number; name: string; avatar?: string; stats?: SubjectStats }
type Analysis = { subject?: Subject; timeseries: TimeseriesPoint[]; wordcloud: { word: string; weight: number }[] }

const dates = reactive({ from: '', to: '' })
const loading = ref(false)
const error = ref('')
const analysis = reactive<Analysis>({ timeseries: [], wordcloud: [] })
const subject = ref<Subject | undefined>(undefined)

function setDefaultDates(days = 7) {
  const to = new Date()
  const from = new Date()
  from.setDate(to.getDate() - (days - 1))
  dates.from = from.toISOString().slice(0, 10)
  dates.to = to.toISOString().slice(0, 10)
}

function onDatesChange(newDates: { from: string; to: string }) {
  dates.from = newDates.from
  dates.to = newDates.to
  loadAnalysis()
}

async function loadAnalysis() {
  loading.value = true
  error.value = ''
  try {
    await bridgeReady()
    const res = await api.get_analysis({ from: dates.from, to: dates.to })
    // 允许后端返回更丰富结构；做兼容合并
    analysis.timeseries = res?.timeseries ?? []
    analysis.wordcloud = res?.wordcloud ?? []
    subject.value = res?.subject ?? subject.value
  } catch (e: any) {
    error.value = e?.message || '加载失败'
  } finally {
    loading.value = false
  }
}

function onWordSelect(word: string) {
  // 预留：点击词云词条的交互，例如筛选/高亮/弹窗
  console.debug('selected word:', word)
}

onMounted(() => {
  if (!dates.from || !dates.to) setDefaultDates(7)
  loadAnalysis()
})
</script>

<style scoped>
.analytics-page { display: flex; flex-direction: column; gap: 16px; }
.page-title h1 { margin: 0 0 8px; color: var(--ct-color-primary); }
.grid { display: grid; grid-template-columns: 1fr 360px; gap: 16px; }
.left, .right, .col { display: flex; flex-direction: column; gap: 16px; }

.card {
  background: #fff;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.card-header, .card-hd { padding: 12px 14px; font-weight: 600; color: var(--ct-color-primary); border-bottom: 1px solid rgba(0,0,0,0.06); }
.card-body, .card-bd { padding: 14px; min-height: 140px; }
.skeleton { color: #888; }
.error { color: #b00020; background: #fde7eb; margin: 8px 14px 14px; padding: 8px 10px; border-radius: 8px; font-size: 13px; }
.btn { padding: 6px 10px; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb; cursor: pointer; }

.bottom { display: grid; grid-template-columns: 1fr; gap: 16px; }
.bottom :deep(.subject-card) { grid-column: span 1; }

@media (max-width: 1024px) {
  .grid { grid-template-columns: 1fr; }
}
</style>
