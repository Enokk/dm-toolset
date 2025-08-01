export interface RouteConfig {
  name: string
  path: string
  label: string
  icon: string
  component: () => Promise<any>
  showInMenu?: boolean
  menuSection?: number
}

export const ROUTES: RouteConfig[] = [
  {
    name: 'home',
    path: '/',
    label: 'Home',
    icon: 'pi pi-home',
    component: () => import('@/views/HomeView.vue'),
    showInMenu: true,
    menuSection: 1
  },
  {
    name: 'characters',
    path: '/characters',
    label: 'Gestione Personaggi',
    icon: 'pi pi-users',
    component: () => import('@/views/CharactersView.vue'),
    showInMenu: true,
    menuSection: 2
  },
  {
    name: 'initiative',
    path: '/initiative',
    label: 'Gestione Iniziativa',
    icon: 'pi pi-sort',
    component: () => Promise.resolve(),
    showInMenu: true,
    menuSection: 2
  },
  {
    name: 'not-found',
    path: '/:pathMatch(.*)*',
    label: 'Pagina non trovata',
    icon: 'pi pi-exclamation-triangle',
    component: () => import('@/views/NotFoundView.vue'),
    showInMenu: false
  }
]

export const getMenuItems = () => {
  return ROUTES.filter(route => route.showInMenu)
}

export const getRoutesForRouter = () => {
  return ROUTES.map(({ name, path, component }) => ({ name, path, component }))
}

export const getPageTitles = () => {
  const titles: Record<string, string> = {}
  ROUTES.forEach(route => {
    titles[route.name] = route.name === 'home' ? 'DM Toolset' : route.label
  })
  return titles
}

export const getMenuItemsGrouped = () => {
  const menuItems = getMenuItems()
  const sections: Record<number, RouteConfig[]> = {}
  
  menuItems.forEach(item => {
    const section = item.menuSection || 1
    if (!sections[section]) {
      sections[section] = []
    }
    sections[section].push(item)
  })
  
  return sections
}