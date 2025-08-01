<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getMenuItemsGrouped } from '@/config/routeConfig'

const router = useRouter()

defineProps<{
  isVisible: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const menuSections = computed(() => {
  return getMenuItemsGrouped()
})

const navigateTo = (path: string) => {
  router.push(path)
  closeMenu()
}

const closeMenu = () => {
  emit('close')
}
</script>

<template>
  <Transition name="backdrop-fade">
    <div 
      v-if="isVisible"
      class="fixed top-[var(--navbar-height)] right-0 bottom-0 left-0 z-40 bg-black/20 backdrop-blur-xs"
      @click="closeMenu"
    />
  </Transition>

  <Transition name="slide-fade">
    <div 
      v-if="isVisible"
      class="fixed top-[var(--navbar-height)] right-4 z-50 mt-4 bg-surface-900 rounded-2xl shadow-2xl w-[var(--menu-width)]"
    >
      <div class="py-2">
        <template v-for="(sectionItems, sectionNumber) in menuSections" :key="sectionNumber">
          <!-- Separatore tra sezioni (tranne per la prima) -->
          <div 
            v-if="sectionNumber > 1"
            class="my-2 mx-4 border-t border-surface-800"
          />
          
          <!-- Items della sezione -->
          <button
            v-for="item in sectionItems"
            :key="item.name"
            @click="navigateTo(item.path)"
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
/* Transizione per il menu */
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

/* Transizione per il backdrop */
.backdrop-fade-enter-active {
  transition: opacity 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.backdrop-fade-leave-active {
  transition: opacity 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.backdrop-fade-enter-from,
.backdrop-fade-leave-to {
  opacity: 0;
}
</style> 