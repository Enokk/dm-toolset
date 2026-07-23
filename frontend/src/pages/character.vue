<script setup lang="ts">
import { ref } from 'vue'

import AbilityScoresCard from '@/components/character/AbilityScoresCard.vue'
import CharacterHeader from '@/components/character/CharacterHeader.vue'
import HitPointsCard from '@/components/character/HitPointsCard.vue'
import { useCharacter } from '@/composables/useCharacter'

const mode = ref<'exploration' | 'combat'>('exploration')

const { character, notFound, updateVitals } = useCharacter(1)
</script>

<template>
  <div class="mx-auto w-350 pt-8">
    <div v-if="character" class="overflow-hidden rounded-lg border border-border">
      <div class="border-b border-border bg-linear-to-b from-muted to-background px-10 pt-8">
        <CharacterHeader
          v-model:mode="mode"
          :name="character.name"
          :character-race="character.character_race.name"
          :character-class="character.character_class.name"
          :level="character.level"
        />
      </div>

      <main class="bg-background px-10 pb-8 pt-8 text-muted-foreground">
        <div class="grid grid-cols-6 gap-4">
          <HitPointsCard
            :current="character.hit_points_current"
            :max="character.hit_points_max"
            :temp="character.hit_points_temp"
            class="col-span-2"
            @change="updateVitals"
          />
        </div>

        <div class="grid grid-cols-8 mt-4">
          <AbilityScoresCard
            :strength="character.strength"
            :dexterity="character.dexterity"
            :constitution="character.constitution"
            :intelligence="character.intelligence"
            :wisdom="character.wisdom"
            :charisma="character.charisma"
            class="col-span-2"
          />
        </div>
      </main>
    </div>

    <p v-else-if="notFound" class="text-destructive">Personaggio non trovato.</p>
  </div>
</template>
