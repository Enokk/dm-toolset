<script setup lang="ts">
import AppTopbar from '@/layout/AppTopbar.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="h-screen flex flex-col">
    <AppTopbar />
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>