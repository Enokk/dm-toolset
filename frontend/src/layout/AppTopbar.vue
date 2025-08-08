<script setup lang="ts">
import { reactive } from 'vue'
import Menu from '@/components/Menu.vue'
import GradientImage from '@/components/GradientImage.vue'
import { usePageTitle } from '@/composables/usePageTitle'
import logo from '@/assets/images/logo.png'

const { currentPageTitle } = usePageTitle()

const state = reactive({
  isMenuOpen: false
})

const toggleMenu = () => {
  state.isMenuOpen = !state.isMenuOpen
}

const closeMenu = () => {
  state.isMenuOpen = false
}
</script>

<template>
  <nav class="sticky top-0 h-[var(--navbar-height)] z-50 bg-accent px-4 py-3">
    <div class="flex justify-between items-center">
      <div class="flex justify-start min-w-[5%]">
        <RouterLink :to="{ name: 'home' }">
          <GradientImage 
          :image-url="logo"
          alt="logo"
          />
        </RouterLink>
      </div>
      
      <div class="flex-1 flex justify-center">
          <span class="theme-gradient bg-clip-text text-transparent text-3xl font-bold cursor-default">
            {{ currentPageTitle }}
          </span>
      </div>

      <div class="flex justify-end min-w-[5%]">
            <Button 
            text
            icon="pi pi-bars"
            size="large"
            severity="info"
            @click="toggleMenu"
            />
      </div>
    </div>
    
    <Menu 
      :is-visible="state.isMenuOpen"
      @close="closeMenu"
    />
  </nav>
</template> 