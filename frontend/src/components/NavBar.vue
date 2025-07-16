<script setup lang="ts">
import { reactive } from 'vue'

const state = reactive({
  isMenuOpen: false
})

const toggleMenu = () => {
  state.isMenuOpen = !state.isMenuOpen
}
</script>

<template>
  <nav class="sticky top-0 z-50 bg-gray-900 border-b border-gray-700 px-4 py-3">
    <div class="flex justify-between items-center">
      <div class="flex justify-start min-w-[5%]">
        <img src="@/assets/logo.png" alt="logo" class="w-10 h-10">
      </div>

      <div class="flex-1 flex justify-center">
        <span class="bg-gradient-to-r from-[#20D6DE] via-[#7190D8] to-[#C24AD2] bg-clip-text text-transparent text-2xl font-bold">
          DM Toolset
        </span>
      </div>

      <div class="flex justify-end min-w-[5%]">
        <button 
          @click="toggleMenu"
          class="text-(--p-primary-color)"
        >
          <i class="pi pi-bars !text-3xl"></i>
        </button>
      </div>
    </div>
  </nav>
</template> 