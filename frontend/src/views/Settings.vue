<template>
  <section class="settings-page">
    <header class="page-title">
      <h1>设置</h1>
      <div class="_actions">
        <CtButton variant="ghost" :loading="loading" @click="onLoad">读取</CtButton>
        <CtButton :loading="saving" @click="onSave">保存</CtButton>
      </div>
    </header>

    <div class="grid">
      <!-- 通用配置 -->
      <CtCard title="通用配置">
        <template #default>
          <div class="form">
            <label class="row">
              <div class="lab">模型</div>
              <select v-model="form.model" class="ct-field">
                <option value="local">本地/内置</option>
                <option value="openai-gpt-4o">OpenAI · GPT-4o</option>
                <option value="qwen">阿里 · 通义千问</option>
                <option value="moonshot">Moonshot</option>
              </select>
            </label>

            <label class="row">
              <div class="lab">API Token</div>
              <CtField v-model="form.api_token" placeholder="用于访问所选模型的 API Token（保存在本地）" />
            </label>
          </div>
        </template>
        <template #footer>
          <small class="hint">提示：不同模型供应商可能需要在后端设置额外 Base URL 或代理；本页仅保存 Token 与模型类型。</small>
        </template>
      </CtCard>

      <!-- 消息抓取与监听 -->
      <CtCard title="消息抓取与监听">
        <div class="form">
          <label class="row">
            <div class="lab">抓取间隔（分钟）</div>
            <input v-model.number="form.interval_minutes" type="number" min="1" step="1" class="ct-field" placeholder="如：15" />
          </label>

          <label class="row">
            <div class="lab">每次最大抓取条数</div>
            <input v-model.number="form.batch_size" type="number" min="10" step="10" class="ct-field" placeholder="如：100" />
          </label>

          <label class="row">
            <div class="lab">启用实时监听</div>
            <input v-model="form.realtime_enabled" type="checkbox" />
          </label>
        </div>
      </CtCard>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { bridgeReady, api } from '@/api/bridge'
import CtCard from '@/components/base/CtCard.vue'
import CtField from '@/components/base/CtField.vue'
import CtButton from '@/components/base/CtButton.vue'

const loading = ref(false)
const saving = ref(false)
const form = reactive<{ model: string; api_token: string; interval_minutes: number; batch_size: number; realtime_enabled: boolean }>({
  model: 'local',
  api_token: '',
  interval_minutes: 15,
  batch_size: 100,
  realtime_enabled: true,
})

async function onLoad() {
  loading.value = true
  try {
    await bridgeReady()
    const s = await api.get_settings()
    if (s && typeof s === 'object') {
      form.model = s.model ?? form.model
      form.api_token = s.api_token ?? form.api_token
      form.interval_minutes = Number(s.interval_minutes ?? form.interval_minutes)
      form.batch_size = Number(s.batch_size ?? form.batch_size)
      form.realtime_enabled = Boolean(s.realtime_enabled ?? form.realtime_enabled)
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function onSave() {
  saving.value = true
  try {
    await bridgeReady()
    await api.set_settings({
      model: form.model,
      api_token: form.api_token,
      interval_minutes: form.interval_minutes,
      batch_size: form.batch_size,
      realtime_enabled: form.realtime_enabled,
    })
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

onMounted(() => { onLoad() })
</script>

<style scoped>
.settings-page { display: flex; flex-direction: column; gap: 16px; }
.page-title { display: flex; align-items: center; justify-content: space-between; }
.page-title h1 { margin: 0; color: var(--ct-color-primary); }
._actions { display: inline-flex; gap: 8px; }

.grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.form { display: flex; flex-direction: column; gap: 12px; }
.row { display: grid; grid-template-columns: 160px 1fr; gap: 12px; align-items: center; }
.lab { color: #555; }
.hint { color: #666; }
</style>
