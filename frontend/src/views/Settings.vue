<template>
  <section>
    <h1>设置</h1>
    <button @click="load">读取设置</button>
    <button @click="save">保存设置</button>
    <pre v-if="settings">{{ settings }}</pre>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'

const settings = ref<any>('')

async function load() {
  await bridgeReady()
  settings.value = await api.get_settings()
}

async function save() {
  await bridgeReady()
  settings.value = await api.set_settings({ model: 'local', interval_minutes: 15 })
}
</script>
