<script setup lang="ts">
import { useRouter } from 'vue-router'
import GradientImage from '@/components/GradientImage.vue'
import img404 from '@/assets/images/404.png'
const router = useRouter()

const goHome = () => {
  router.push({ name: 'home' })
}

const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="flex flex-col items-center h-full gap-12 m-24">
    <GradientImage 
      :image-url="img404"
      alt="404"
      width="w-80" 
      height="h-80"
    />
    
    <div class="text-center">
      <p class="text-lg text-muted-color max-w-md">
        Ops! La pagina che stai cercando non esiste o è stata spostata.
      </p>
    </div>
    
    <div class="flex gap-4 flex-wrap justify-center">
      <Button 
        type="button" 
        label="Torna alla Home" 
        @click="goHome"
        class="px-6 py-3"
      />
      <Button 
        type="button" 
        label="Torna indietro" 
        @click="goBack"
        severity="secondary"
        class="px-6 py-3"
      />
    </div>
  </div>
</template> 