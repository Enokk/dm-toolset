<script setup lang="ts">
import { ref } from 'vue'

import { apiClient } from '@/api/client'
import CharacterHeader from '@/components/character/CharacterHeader.vue'
import type { components } from '@/api/schema.d.ts'

const mode = ref<'exploration' | 'combat'>('exploration')

const character = ref<components['schemas']['CharacterPublic'] | null>(null)
const notFound = ref(false)

// TODO: hardcoded until character selection/routing exists.
apiClient.GET('/api/characters/{character_id}', { params: { path: { character_id: 1 } } }).then(({ data, error }) => {
  character.value = data ?? null
  notFound.value = !!error
})
</script>

<template>
  <div class="mx-auto w-[1800px] pt-8">
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
        {{ mode === 'exploration' ? "Contenuto di esplorazione in arrivo." : "Contenuto di combattimento in arrivo." }}

      </main>
    </div>

    <p v-else-if="notFound" class="text-destructive">Personaggio non trovato.</p>
  </div>
</template>
