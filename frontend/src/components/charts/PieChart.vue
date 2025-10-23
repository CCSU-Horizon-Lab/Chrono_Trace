<template>
  <div :style="{ width: '100%', height: h }" ref="el"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import * as echarts from 'echarts'
const props = withDefaults(defineProps<{ data: { name: string; value: number }[]; colors?: string[]; height?: number|string }>(), {
  colors: () => ['#7AB8BF', '#F2C14E', '#E77F67', '#9DB17C', '#A18CD1'], height: 260
})
const h = computed(() => typeof props.height === 'number' ? props.height + 'px' : props.height)
const el = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null
function render() {
  if (!el.value) return
  if (!chart) chart = echarts.init(el.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{ type: 'pie', name: '情绪', radius: '55%', data: props.data, label: { formatter: '{b}: {d}%' }, color: props.colors,
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.2)' } } }]
  })
}
function resize(){ chart && chart.resize() }
onMounted(() => { render(); window.addEventListener('resize', resize) })
onBeforeUnmount(() => { window.removeEventListener('resize', resize); if (chart) { chart.dispose(); chart = null } })
watch(() => props.data, () => render(), { deep: true })
</script>
