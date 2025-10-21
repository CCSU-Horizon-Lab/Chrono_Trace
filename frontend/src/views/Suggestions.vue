<template>
  <section>
    <h1>建议</h1>
    <select v-model="intent">
      <option value="intimate">亲密</option>
      <option value="maintain">维持</option>
      <option value="distance">疏远</option>
    </select>
    <button @click="gen">生成示例建议</button>
    <pre v-if="res">{{ res }}</pre>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'

const intent = ref('maintain')
const res = ref<any>('')

async function gen() {
  await bridgeReady()
  res.value = await api.generate_suggestion(intent.value, { recent: [] })
}
</script>
