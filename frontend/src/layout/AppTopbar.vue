<script setup lang="ts">
import { reactive } from 'vue'
import Menu from '@/components/Menu.vue'
import GradientImage from '@/components/GradientImage.vue'
import logo from '@/assets/images/logo.png'

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
        <GradientImage 
        :image-url="logo"
        alt="logo"
        />
      </div>
      
      <div class="flex-1 flex justify-center">
        <RouterLink :to="{ name: 'home' }">
          <span class="theme-gradient bg-clip-text text-transparent text-3xl font-bold">
            DM Toolset
          </span>
        </RouterLink>
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