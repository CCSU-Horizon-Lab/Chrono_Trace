import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Analytics from '@/views/Analytics.vue'
import Suggestions from '@/views/Suggestions.vue'
import Settings from '@/views/Settings.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/analytics', component: Analytics },
    { path: '/suggestions', component: Suggestions },
    { path: '/settings', component: Settings }
  ]
})

export default router
