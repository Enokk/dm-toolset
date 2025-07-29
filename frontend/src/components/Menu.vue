<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()

defineProps<{
  isVisible: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const menuItems = [
  { label: 'Home', icon: 'pi pi-home', action: () => navigateTo('/') },
  { label: 'Gestione Personaggi', icon: 'pi pi-users', action: () => navigateTo('/characters') },
  { label: 'Campagne', icon: 'pi pi-calendar', action: () => navigateTo('/campaigns') },
  { separator: true },
  { label: 'Mappe', icon: 'pi pi-map', action: () => navigateTo('/maps') },
  { label: 'Inventario', icon: 'pi pi-box', action: () => navigateTo('/inventory') },
  { separator: true },
  { label: 'Dadi', icon: 'pi pi-circle', action: () => navigateTo('/dice') },
  { label: 'Note', icon: 'pi pi-file-edit', action: () => navigateTo('/notes') },
  { separator: true },
  { label: 'Impostazioni', icon: 'pi pi-cog', action: () => navigateTo('/settings') },
  { label: 'Aiuto', icon: 'pi pi-question-circle', action: () => navigateTo('/help') }
]

const navigateTo = (path: string) => {
  router.push(path)
  closeMenu()
}

const closeMenu = () => {
  emit('close')
}
</script>

<template>
  <div 
    v-if="isVisible"
    class="fixed top-[var(--navbar-height)] right-0 bottom-0 left-0 z-40 bg-black/20 backdrop-blur-xs"
    @click="closeMenu"
  />

  <Transition name="slide-fade">
    <div 
      v-if="isVisible"
      class="fixed top-[var(--navbar-height)] right-4 z-50 mt-4 bg-surface-900 rounded-2xl shadow-2xl w-[var(--menu-width)]"
    >
      <div class="py-2">
        <template v-for="(item, index) in menuItems" :key="index">
          <div 
            v-if="item.separator" 
            class="my-2 mx-4 border-t border-surface-800"
          />
          
          <button
            v-else
            @click="item.action"
            class="w-full px-6 py-3 flex items-center gap-4 text-left hover:bg-surface-800 transition-all duration-200 group"
          >
            <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-surface-800 group-hover:bg-primary-900/30 transition-colors duration-200">
              <i 
                :class="item.icon" 
                class="text-surface-300 group-hover:text-primary-400 transition-colors duration-200"
              />
            </div>
            <span class="text-surface-200 font-medium group-hover:text-surface-50 transition-colors duration-200">
              {{ item.label }}
            </span>
          </button>
        </template>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}
</style> 