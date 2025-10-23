<template>
  <section class="suggs">
    <header class="page-title">
      <h1>AI 建议</h1>
    </header>

    <div class="grid">
      <div class="left">
        <!-- 1) 发展走向选择卡 -->
        <div class="card">
          <div class="ct-card-hd">发展走向</div>
          <div class="card-bd intent-row">
            <div class="seg">
              <label>
                <input type="radio" value="intimate" v-model="intent" /> 亲密
              </label>
              <label>
                <input type="radio" value="maintain" v-model="intent" /> 维持
              </label>
              <label>
                <input type="radio" value="distance" v-model="intent" /> 疏远
              </label>
            </div>
            <button class="ct-btn" :disabled="loading" @click="gen">
              <span v-if="!loading">生成建议</span>
              <span v-else>生成中…</span>
            </button>
          </div>
          <p class="hint">将根据你的目标倾向，给出更贴合的沟通策略。</p>
          <p v-if="error" class="error">{{ error }}</p>
        </div>

        <!-- 2) AI 建议与对话卡 -->
        <div class="ct-card chat">
          <div class="card-hd tools">
            <div class="title">建议与对话</div>
            <div class="actions">
              <CtButton variant="ghost" @click="onRefresh" :disabled="loading">刷新</CtButton>
              <CtButton variant="ghost" @click="onClear">清空</CtButton>
              <CtButton variant="ghost" @click="copyAll" :disabled="!suggestion">复制</CtButton>
            </div>
          </div>
          <div class="card-bd chat-body">
            <div v-if="!suggestion && !loading" class="empty">暂无建议，点击上方“生成建议”。</div>
            <div v-if="loading" class="skeleton">AI 正在思考…</div>
            <template v-if="suggestion">
              <div class="bubble ai">
                <div class="summary" v-if="suggestion.summary">{{ suggestion.summary }}</div>
                <ul class="speech" v-if="suggestion.speech && suggestion.speech.length">
                  <li v-for="(sp, i) in suggestion.speech" :key="i">
                    <span>{{ sp }}</span>
                    <button class="mini" @click="copyText(sp)">复制</button>
                  </li>
                </ul>
              </div>
              <div v-for="(m, i) in messages" :key="i" :class="['bubble', m.role]">{{ m.content }}</div>
            </template>
          </div>
          <div class="chat-input">
            <input v-model="userInput" type="text" placeholder="补充你的背景/需求，回车发送" @keydown.enter.exact.prevent="send" />
            <button class="ct-btn" @click="send" :disabled="!userInput.trim() || loading">发送</button>
          </div>
        </div>
      </div>

      <div class="right">
        <!-- 3) 对象信息卡 -->
        <div class="card">
          <div class="ct-card-hd">对象信息</div>
          <div class="card-bd profile">
            <div class="avatar" aria-hidden="true">{{ profileInitial }}</div>
            <div class="meta">
              <div class="name">{{ profile.name || '未命名对象' }}</div>
              <div class="tags" v-if="profile.tags && profile.tags.length">
                <span v-for="t in profile.tags" :key="t">{{ t }}</span>
              </div>
              <div class="stats">
                <div>近7天互动：{{ profile.stats?.interactions7d ?? '-' }}</div>
                <div>平均响应：{{ profile.stats?.avgLatency ?? '-' }}</div>
              </div>
            </div>
          </div>
          <div class="note" v-if="profile.note">{{ profile.note }}</div>
        </div>

        <!-- 4) 情绪分析（饼图） -->
        <div class="card">
          <div class="ct-card-hd">情绪占比（近期）</div>
          <div class="card-bd">
            <div v-if="!emotions.length" class="empty">暂无数据，待导入或等待实时生成</div>
            <div v-else ref="pieRef" class="pie"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount, computed } from 'vue'
import { bridgeReady, api } from '@/api/bridge'
import * as echarts from 'echarts'

type Message = { role: 'ai' | 'user'; content: string }

const intent = ref<'intimate' | 'maintain' | 'distance'>('maintain')
const loading = ref(false)
const error = ref('')
const suggestion = ref<{ summary?: string; speech?: string[] } | null>(null)
const messages = ref<Message[]>([])
const userInput = ref('')

// 临时占位：对象信息与情绪数据（后端接好前可替换）
const profile = ref<{ name?: string; tags?: string[]; stats?: any; note?: string }>({
  name: '对方昵称',
  tags: ['朋友'],
  stats: { interactions7d: 12, avgLatency: '15m' },
  note: '最近工作压力大，回复不稳定。'
})
const profileInitial = computed(() => (profile.value.name ? profile.value.name[0] : 'N'))

const emotions = ref<{ name: string; value: number }[]>([
  { name: '积极', value: 40 },
  { name: '中性', value: 35 },
  { name: '消极', value: 25 }
])


async function gen() {
  loading.value = true
  error.value = ''
  try {
    await bridgeReady()
    const r = await api.generate_suggestion(intent.value, { recent: [] })
    suggestion.value = r || null
  } catch (e: any) {
    error.value = e?.message || '生成失败，请重试'
  } finally {
    loading.value = false
  }
}

function onRefresh() { if (!loading.value) gen() }
function onClear() { suggestion.value = null; messages.value = []; userInput.value = '' }
function copyText(text: string) { navigator.clipboard?.writeText(text) }
function copyAll() {
  if (!suggestion.value) return
  const txt = [suggestion.value.summary || '', ...(suggestion.value.speech || [])].filter(Boolean).join('\n')
  navigator.clipboard?.writeText(txt)
}

async function send() {
  const content = userInput.value.trim()
  if (!content) return
  messages.value.push({ role: 'user', content })
  userInput.value = ''
  loading.value = true
  error.value = ''
  try {
    await bridgeReady()
    const r = await api.generate_suggestion(intent.value, { recent: messages.value })
    suggestion.value = r || null
    messages.value.push({ role: 'ai', content: r?.summary || '已更新建议，请查看上方内容。' })
  } catch (e: any) {
    error.value = e?.message || '发送失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.suggs { display: flex; flex-direction: column; gap: 16px; }
.page-title h1 { margin: 0 0 8px; color: var(--ct-color-primary); }
.grid { display: grid; grid-template-columns: 1fr 360px; gap: 16px; }
.left, .right { display: flex; flex-direction: column; gap: 16px; }

.card { background: #fff; border: 1px solid rgba(0,0,0,0.06); border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.card-hd { padding: 12px 14px; font-weight: 600; color: var(--ct-color-primary); border-bottom: 1px solid rgba(0,0,0,0.06); }
.card-bd { padding: 14px; }
.hint { color: #666; font-size: 12px; padding: 0 14px 12px; margin: 0; }
.error { color: #b00020; background: #fde7eb; margin: 8px 14px 14px; padding: 8px 10px; border-radius: 8px; font-size: 13px; }

.intent-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.seg { display: flex; gap: 12px; background: var(--ct-color-primary-50); padding: 8px 10px; border-radius: 10px; }
.seg label { display: flex; align-items: center; gap: 6px; }


.mini { border: none; background: transparent; color: var(--ct-color-primary); cursor: pointer; }

.chat .tools { display: flex; align-items: center; justify-content: space-between; }
.chat-body { display: flex; flex-direction: column; gap: 10px; min-height: 140px; }
.bubble { max-width: 100%; padding: 10px 12px; border-radius: 12px; }
.bubble.ai { background: #f6f7fb; align-self: flex-start; }
.bubble.user { background: var(--ct-color-accent); color: #1F2430; align-self: flex-end; }
.summary { font-weight: 600; margin-bottom: 8px; }
.speech { display: flex; flex-direction: column; gap: 8px; padding-left: 16px; }
.speech li { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.skeleton { color: #888; }
.empty { color: #888; }
.chat-input { display: flex; gap: 8px; padding: 12px 14px; border-top: 1px solid rgba(0,0,0,0.06); }

.profile { display: flex; gap: 12px; align-items: center; }
.avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--ct-color-accent); display: flex; align-items: center; justify-content: center; color: #1F2430; font-weight: 700; }
.meta .name { font-weight: 600; margin-bottom: 4px; }
.tags { display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0; }
.tags span { background: var(--ct-color-primary-50); color: var(--ct-color-primary); padding: 2px 6px; border-radius: 6px; font-size: 12px; }
.stats { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12px; color: #555; }
.note { padding: 0 14px 14px; color: #555; font-size: 13px; }

.pie { width: 100%; height: 260px; }

@media (max-width: 1024px) {
  .grid { grid-template-columns: 1fr; }
}
</style>
