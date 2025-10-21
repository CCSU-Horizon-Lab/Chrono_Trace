<template>
  <section>
    <h1>情绪数据</h1>
    <button @click="load">加载示例分析</button>
    <pre v-if="data">{{ data }}</pre>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'

const data = ref<any>('')

async function load() {
  await bridgeReady()
  data.value = await api.get_analysis({ from: '2025-01-01', to: '2025-01-07' })
}
</script>
