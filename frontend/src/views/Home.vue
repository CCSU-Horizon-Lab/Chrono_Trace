<template>
  <section class="home-page">
    <!-- 标题与介绍 -->
    <header class="page-title">
      <h1>首页</h1>
    </header>

    <div class="grid">
      <!-- 应用介绍 -->
      <CtCard title="关于 Chrono_Trace">
        <template #default>
          <p class="slogan">“镌刻对话年轮，丈量心动间距”</p>
          <ul class="intro">
            <li>导入历史聊天数据，生成情绪曲线、词云与分段总结。</li>
            <li>结合近期对话，提供个性化沟通建议（亲密/维持/疏远）。</li>
            <li>设置中可配置模型、API Token 与抓取策略。</li>
          </ul>
        </template>
      </CtCard>

      <!-- 新手引导/快速开始 -->
      <CtCard title="快速开始">
        <div class="form">
          <label class="row">
            <div class="lab">对象名称</div>
            <CtField v-model="form.subject" placeholder="例如：小林 / Alex" />
          </label>
          <label class="row">
            <div class="lab">数据源路径</div>
            <CtField v-model="form.data_path" placeholder="例如：C:/data/chat/history.json 或导出目录" />
          </label>
          <div class="actions">
            <CtButton :loading="importing" @click="onImport">导入数据</CtButton>
            <CtButton variant="ghost" :loading="pinging" @click="ping">测试桥接</CtButton>
          </div>
          <p v-if="err" class="error">{{ err }}</p>
          <p v-if="ok" class="ok">{{ ok }}</p>
        </div>
      </CtCard>

      <!-- 运行日志 -->
      <CtCard title="运行日志">
        <div class="logs">
          <div v-if="!logs.length" class="empty">暂无日志</div>
          <ul v-else>
            <li v-for="(l, i) in logs" :key="i">
              <span class="ts">{{ l.ts }}</span>
              <span class="msg">{{ l.msg }}</span>
            </li>
          </ul>
        </div>
      </CtCard>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { bridgeReady, api } from '@/api/bridge'
import CtCard from '@/components/base/CtCard.vue'
import CtField from '@/components/base/CtField.vue'
import CtButton from '@/components/base/CtButton.vue'

const form = reactive({ subject: '', data_path: '' })
const logs = ref<{ ts: string; msg: string }[]>([])
const err = ref('')
const ok = ref('')
const importing = ref(false)
const pinging = ref(false)

function addLog(msg: string) {
  const ts = new Date().toLocaleString()
  logs.value.unshift({ ts, msg })
}

async function onImport() {
  err.value = ''
  ok.value = ''
  if (!form.data_path.trim()) { err.value = '请填写数据源路径'; return }
  importing.value = true
  try {
    await bridgeReady()
    const res = await api.ingest_data(form.data_path, { subject: form.subject || '默认对象' })
    addLog('导入完成')
    ok.value = typeof res === 'string' ? res : '导入成功'
  } catch (e: any) {
    err.value = e?.message || '导入失败'
    addLog('导入失败')
  } finally {
    importing.value = false
  }
}

const pong = ref('')
async function ping() {
  pinging.value = true
  try {
    await bridgeReady()
    pong.value = await api.ping()
    addLog('桥接可用: ' + pong.value)
  } catch (e: any) {
    err.value = e?.message || '桥接失败'
    addLog('桥接失败')
  } finally {
    pinging.value = false
  }
}
</script>

<style scoped>
.home-page { display: flex; flex-direction: column; gap: 16px; }
.page-title { display: flex; align-items: center; justify-content: space-between; }
.page-title h1 { margin: 0; color: var(--ct-color-primary); }
.grid { display: grid; grid-template-columns: 1fr; gap: 16px; }

.slogan { margin: 0 0 8px; font-weight: 700; color: var(--ct-color-primary); }
.intro { margin: 8px 14px; padding-left: 16px; color: #555; }
.intro li { margin: 6px 0; }

.form { display: flex; flex-direction: column; gap: 12px; }
.row { display: grid; grid-template-columns: 140px 1fr; gap: 12px; align-items: center; }
.lab { color: #555; }
.actions { display: inline-flex; gap: 8px; }
.error { color: #b00020; background: #fde7eb; padding: 8px 10px; border-radius: 8px; }
.ok { color: #0c7c3a; background: #e8f5ec; padding: 8px 10px; border-radius: 8px; }

.logs { padding: 4px 0; max-height: 220px; overflow: auto; }
.logs ul { list-style: none; padding: 0 14px; margin: 0; display: flex; flex-direction: column; gap: 6px; }
.logs .ts { color: #888; margin-right: 8px; font-size: 12px; }
.logs .msg { color: #333; }
.empty { color: #888; padding: 0 14px 12px; }
</style>
