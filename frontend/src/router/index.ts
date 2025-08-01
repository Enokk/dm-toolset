import { createRouter, createWebHistory } from 'vue-router'
import { getRoutesForRouter } from '@/config/routeConfig'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: getRoutesForRouter()
})

export default router
