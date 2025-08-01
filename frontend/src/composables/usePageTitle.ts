import { computed, readonly } from 'vue'
import { useRoute } from 'vue-router'
import { getPageTitles } from '@/config/routeConfig'

const PAGE_TITLES = getPageTitles()
const DEFAULT_TITLE = 'DM Toolset'

export function usePageTitle() {
  const route = useRoute()
  
  const currentPageTitle = computed(() => {
    const routeName = route.name as string
    return PAGE_TITLES[routeName] || DEFAULT_TITLE
  })
  
  const getTitleByRouteName = (routeName: string): string => {
    return PAGE_TITLES[routeName] || DEFAULT_TITLE
  }
  
  return {
    currentPageTitle,
    getTitleByRouteName,
    PAGE_TITLES: readonly(PAGE_TITLES)
  }
}