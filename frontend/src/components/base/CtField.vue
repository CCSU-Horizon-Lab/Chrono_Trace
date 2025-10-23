<template>
  <component :is="tag" class="ct-field" :rows="rows" :placeholder="placeholder" :value="modelValue" @input="onInput" />
</template>
<script setup lang="ts">
import { computed } from 'vue'
const props = withDefaults(defineProps<{ modelValue: string; placeholder?: string; textarea?: boolean; rows?: number }>(), {
  placeholder: '', textarea: false, rows: 3
})
const emit = defineEmits<{ (e:'update:modelValue', v:string):void }>()
const tag = computed(() => props.textarea ? 'textarea' : 'input')
function onInput(e: Event) { emit('update:modelValue', (e.target as HTMLInputElement).value) }
</script>
