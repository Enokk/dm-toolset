<script setup lang="ts">
import { reactive, onMounted } from 'vue'

interface Character {
  id: number
  name: string
  class: string
  level: number
  image: string
  stats: {
    name: string
    value: number
  }[]
  skills: {
    name: string
    value: string
  }[]
  hitPoints: number
  armorClass: number
}

const state = reactive({
  characters: [] as Character[],
  loading: true,
  error: null as string | null
})

const fetchCharacters = async () => {
  try {
    state.loading = true
    state.error = null
    
    const response = await fetch(import.meta.env.VITE_API_URL + 'characters')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Mappa i dati dall'API al formato del frontend
    state.characters = data.map((char: any) => ({
      id: char.id,
      name: char.name,
      class: char.character_class, // Il modello usa character_class
      level: char.level,
      image: import.meta.env.VITE_BASE_URL + char.image,
      // Trasforma gli stats da dizionario ad array
      stats: Object.entries(char.stats || {}).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1), // Capitalizza la prima lettera
        value: value as number
      })),
      // Trasforma le skills da dizionario ad array  
      skills: Object.entries(char.skills || {}).map(([name, value]) => ({
        name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), // Trasforma snake_case in Title Case
        value: `${(value as number > 0) ? '+' : ''}${value}` as string
      })),
      hitPoints: char.hit_points,
      armorClass: char.armor_class
    }))
    
  } catch (err) {
    state.error = 'Errore nel caricamento dei personaggi'
  } finally {
    state.loading = false
  }
}

onMounted(() => {
  fetchCharacters()
})

const getStatModifier = (stat: number): string => {
  const modifier = Math.floor((stat - 10) / 2)
  return modifier >= 0 ? `+${modifier}` : `${modifier}`
}
</script>

<template>
  <div class="p-8 min-h-full bg-surface-ground">
    <!-- Loading state -->
    <div v-if="state.loading" class="flex justify-center items-center h-64">
      <div class="text-2xl">Caricamento personaggi...</div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="state.error" class="flex justify-center items-center h-64">
      <div class="text-2xl text-red-500">{{ state.error }}</div>
    </div>
    
    <!-- Characters grid -->
    <div v-else class="grid grid-cols-4 gap-8">
      <div 
        v-for="character in state.characters" 
        :key="character.id"
        class="bg-accent rounded-2xl overflow-hidden hover:scale-101 transition-transform duration-200"
      >
        <div class="p-4 space-y-4 flex-1">
          <div class="grid grid-cols-3 gap-3 ">
            <div class="flex flex-row justify-center items-center gap-3 bg-primary-400 rounded-lg text-center py-4 text-primary-950">
              <i class="pi pi-heart text-2xl"></i>
              <div class="text-2xl font-bold">{{ character.hitPoints }}</div>
            </div>
            <div class="flex flex-row justify-center items-center gap-3 bg-primary-400 rounded-lg text-center py-4 text-primary-950">
              <i class="pi pi-shield text-2xl"></i>
              <div class="text-2xl font-bold">{{ character.armorClass }}</div>
            </div>
            <div class="flex flex-row justify-center items-center gap-3 bg-primary-400 rounded-lg text-center py-4 text-primary-950">
              <i class="pi pi-eye text-2xl"></i>
              <div class="text-2xl font-bold">{{ parseInt(character.skills.find(s => s.name === 'Percezione')?.value || '0') + 10 }}</div>
            </div>
          </div>

          <hr class="my-4 border-surface-700"></hr>

          <div class="grid grid-cols-7 gap-3">
            <div class="col-span-3 flex flex-col gap-3">
              <div class="flex flex-col justify-center gap-1 rounded-lg bg-gradient-to-br from-primary-500 to-primary-400 p-4">
                <img 
                  :src="character.image" 
                  :alt="character.name"
                  class="w-32 h-32 rounded-full border border-primary-950 shadow-xl mx-auto"
                />
                <div class="flex-1">
                  <h3 class="font-bold text-2xl text-primary-950">{{ character.name }}</h3>
                  <p class="text-primary-950">{{ character.class }} • Lv {{ character.level }}</p>
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <div v-for="stat in character.stats" :key="stat.name">
                  <div class="flex flex-row justify-between items-center bg-surface-800 rounded-lg h-16 px-4">
                    <div class="w-1/3 text-xl">{{ stat.name }}</div>
                    <div class="w-1/5 text-center rounded-lg bg-surface-900 px-2 py-1">{{ stat.value }}</div>
                    <div class="w-1/4 text-xl font-bold text-center rounded-lg bg-primary-400 px-2 py-1 text-primary-950">{{ getStatModifier(stat.value) }}</div>
                  </div>
                </div>
              </div>            
            </div>
            <div class="col-span-4 flex flex-col gap-3">
              <div class="flex flex-col gap-3">
                <div v-for="skill in character.skills" :key="skill.name">
                  <div class="flex flex-row justify-between items-center bg-surface-800 rounded-lg h-16 px-4">
                    <div class="text-lg">{{ skill.name }}</div>
                    <div class="w-1/4 text-xl font-bold text-center rounded-lg bg-primary-400 px-2 py-1 text-primary-950">{{ skill.value }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  cursor: default;
}
</style>