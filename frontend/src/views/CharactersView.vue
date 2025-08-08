<script setup lang="ts">
import { ref } from 'vue'

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

// Dati mock per la dimostrazione
const characters = ref<Character[]>([
  {
    id: 1,
    name: "Aragorn",
    class: "Ranger",
    level: 12,
    image: "/src/assets/images/logo.png", // placeholder
    stats: [
      { name: "FOR", value: 18 },
      { name: "DES", value: 16 },
      { name: "COS", value: 14 },
      { name: "INT", value: 12 },
      { name: "SAG", value: 15 },
      { name: "CAR", value: 13 }
    ],
         skills: [
       { name: "Furtività", value: "+3" },
       { name: "Indagare", value: "+1" },
       { name: "Intuizione", value: "+2" },
       { name: "Percezione", value: "+4" },
       { name: "Religione", value: "+0" },
       { name: "Storia", value: "+2" }
     ],
    hitPoints: 108,
    armorClass: 17
  },
  {
    id: 2,
    name: "Legolas",
    class: "Fighter",
    level: 11,
    image: "/src/assets/images/logo.png", // placeholder
    stats: [
      { name: "FOR", value: 14 },
      { name: "DES", value: 20 },
      { name: "COS", value: 13 },
      { name: "INT", value: 12 },
      { name: "SAG", value: 17 },
      { name: "CAR", value: 14 }
    ],
    skills: [
      { name: "Furtività", value: "+5" },
      { name: "Indagare", value: "+2" },
      { name: "Intuizione", value: "+3" },
      { name: "Percezione", value: "+4" },
      { name: "Religione", value: "+1" },
      { name: "Storia", value: "+2" }
    ],
    hitPoints: 95,
    armorClass: 18
  },
  {
    id: 3,
    name: "Gandalf",
    class: "Wizard",
    level: 15,
    image: "/src/assets/images/logo.png", // placeholder
    stats: [
      { name: "FOR", value: 10 },
      { name: "DES", value: 14 },
      { name: "COS", value: 12 },
      { name: "INT", value: 20 },
      { name: "SAG", value: 18 },
      { name: "CAR", value: 16 }
    ],
    skills: [
      { name: "Furtività", value: "+2" },
      { name: "Indagare", value: "+5" },
      { name: "Intuizione", value: "+4" },
      { name: "Percezione", value: "+4" },
      { name: "Religione", value: "+5" },
      { name: "Storia", value: "+5" }
    ],
    hitPoints: 78,
    armorClass: 15
  },
  {
    id: 4,
    name: "Gimli",
    class: "Barbarian",
    level: 10,
    image: "/src/assets/images/logo.png", // placeholder
    stats: [
      { name: "FOR", value: 19 },
      { name: "DES", value: 12 },
      { name: "COS", value: 18 },
      { name: "INT", value: 8 },
      { name: "SAG", value: 13 },
      { name: "CAR", value: 10 }
    ],
    skills: [
      { name: "Furtività", value: "+1" },
      { name: "Indagare", value: "-1" },
      { name: "Intuizione", value: "+1" },
      { name: "Percezione", value: "+1" },
      { name: "Religione", value: "-1" },
      { name: "Storia", value: "-1" }
    ],
    hitPoints: 125,
    armorClass: 16
  }
])

const getStatModifier = (stat: number): string => {
  const modifier = Math.floor((stat - 10) / 2)
  return modifier >= 0 ? `+${modifier}` : `${modifier}`
}
</script>

<template>
  <div class="p-8 min-h-full bg-surface-ground">
    <div class="grid grid-cols-4 gap-8">
      <div 
        v-for="character in characters" 
        :key="character.id"
        class="bg-accent rounded-2xl overflow-hidden hover:scale-101 transition-transform duration-200"
      >
        <div class="relative h-24 bg-gradient-to-r from-primary-500 to-primary-400 p-4">
          <div class="flex items-start gap-3">
            <img 
              :src="character.image" 
              :alt="character.name"
              class="w-16 h-16 rounded-full border border-primary-950 shadow-xl"
            />
            <div class="flex-1">
              <h3 class="font-bold text-2xl text-primary-950">{{ character.name }}</h3>
              <p class="text-primary-950">{{ character.class }} • Livello {{ character.level }}</p>
            </div>
          </div>
        </div>

        <div class="p-4 space-y-4 flex-1">
          <div class="grid grid-cols-3 gap-3">
            <div class="flex flex-row justify-center items-center gap-3 bg-surface-800 rounded-lg text-center py-4">
              <i class="pi pi-heart text-2xl"></i>
              <div class="text-2xl font-bold">{{ character.hitPoints }}</div>
            </div>
            <div class="flex flex-row justify-center items-center gap-3 bg-surface-800 rounded-lg text-center py-4">
              <i class="pi pi-shield text-2xl"></i>
              <div class="text-2xl font-bold">{{ character.armorClass }}</div>
            </div>
            <div class="flex flex-row justify-center items-center gap-3 bg-surface-800 rounded-lg text-center py-4">
              <i class="pi pi-eye text-2xl"></i>
              <div class="text-2xl font-bold">{{ 10 + parseInt(character.skills.find(s => s.name === 'Percezione')?.value.replace('+', '') || '0') }}</div>
            </div>
          </div>

          <hr class="my-4 border-surface-700"></hr>

          <div class="grid grid-cols-7 gap-3">
            <div class="col-span-3 flex flex-col gap-3">
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