<script setup lang="ts">
import { reactive } from 'vue'
import Menu from '@/components/Menu.vue'


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
        <img src="@/assets/images/logo.png" alt="logo" class="w-10 h-10">
      </div>

      <div class="flex-1 flex justify-center">
        <span class="bg-gradient-to-r from-[#20D6DE] via-[#7190D8] to-[#C24AD2] bg-clip-text text-transparent text-3xl font-bold">
          DM Toolset
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