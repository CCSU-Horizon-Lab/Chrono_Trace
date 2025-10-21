<template>
  <section>
    <h1>首页</h1>
    <p>这是 ChatMind 的前端骨架页面。</p>
    <button @click="ping">测试桥接 (ping)</button>
    <p v-if="pong">桥接返回：{{ pong }}</p>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'

const pong = ref('')

async function ping() {
  await bridgeReady()
  const res = await api.ping()
  pong.value = res
}
</script>
