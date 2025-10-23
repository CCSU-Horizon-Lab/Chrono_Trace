<template>
  <div class="chart">
    <div v-if="!timeseries?.length" class="empty">所选区间暂无数据</div>
    <svg v-else ref="svgEl" :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="none">
      <defs>
        <linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#6366F1" stop-opacity="0.5" />
          <stop offset="100%" stop-color="#6366F1" stop-opacity="0" />
        </linearGradient>
      </defs>
      <polyline :points="points" fill="url(#g)" stroke="none" />
      <polyline :points="linePoints" fill="none" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type TimeseriesPoint = { ts: string; score: number }
const props = defineProps<{ timeseries: TimeseriesPoint[] }>()

const width = 800
const height = 260
const padding = 10
const svgEl = ref<SVGSVGElement | null>(null)

const linePoints = computed(() => buildPolyline(props.timeseries, false))
const points = computed(() => buildPolyline(props.timeseries, true))

function buildPolyline(data: TimeseriesPoint[], close: boolean) {
  if (!data?.length) return ''
  const xs = data.map((_, i) => i)
  const ys = data.map(d => d.score)
  const minY = Math.min(...ys, 0)
  const maxY = Math.max(...ys, 1)
  const scaleX = (width - padding * 2) / Math.max(1, data.length - 1)
  const scaleY = (height - padding * 2)
  const normY = (y: number) => height - padding - (y - minY) / (maxY - minY || 1) * scaleY
  const normX = (x: number) => padding + x * scaleX
  const pts = data.map((d, i) => `${normX(xs[i]).toFixed(2)},${normY(d.score).toFixed(2)}`).join(' ')
  if (!close) return pts
  // area closed to bottom
  return `${padding},${height - padding} ${pts} ${padding + (data.length - 1) * scaleX},${height - padding}`
}
</script>

<style scoped>
.chart { width: 100%; height: 280px; }
svg { width: 100%; height: 100%; display: block; }
.empty { color: #6b7280; }
</style>
