<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/NavBar.vue'
</script>

<template>
  <div class="h-screen flex flex-col">
    <Navbar />
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>