<template>
  <section class="ct-card">
    <header v-if="hasHeader" class="ct-card-hd">
      <slot name="header">
        <span>{{ title }}</span>
        <div class="_actions"><slot name="actions" /></div>
      </slot>
    </header>
    <div class="ct-card-bd">
      <slot />
    </div>
    <footer v-if="$slots.footer" class="ct-card-ft">
      <slot name="footer" />
    </footer>
  </section>
</template>
<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ title?: string }>()
const hasHeader = computed(() => !!props.title || !!useSlots().header || !!useSlots().actions)
</script>
<style scoped>
.ct-card-ft { padding: 12px 14px; border-top: var(--ct-border); }
._actions { margin-left: auto; display: inline-flex; gap: 8px; }
</style>
