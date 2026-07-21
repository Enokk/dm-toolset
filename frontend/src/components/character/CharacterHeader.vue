<script setup lang="ts">
import { Compass, Swords, UserRound } from '@lucide/vue'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const { name, characterRace, characterClass, level, portraitUrl, specialization } = defineProps<{
  name: string
  characterRace: string
  characterClass: string
  level: number
  portraitUrl?: string | null
  specialization?: string | null
}>()

const mode = defineModel<'exploration' | 'combat'>('mode', { required: true })

</script>

<template>
  <header class="flex items-end justify-between pb-6">
    <div class="flex items-start gap-4">
      <div class="size-24 shrink-0 overflow-hidden rounded-lg border-2 border-border bg-muted">
        <img
          v-if="portraitUrl"
          :src="portraitUrl"
          :alt="name"
          class="h-full w-full object-cover"
        >
        <div v-else class="flex h-full w-full items-center justify-center">
          <UserRound class="size-13 text-muted-foreground" />
        </div>
      </div>

      <div>
        <h1 class="text-3xl font-bold tracking-tight">{{ name }}</h1>
        <p class="mt-2 text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
          {{ characterRace }} · {{ characterClass }} · Livello {{ level }}
        </p>

        <Badge
          v-if="specialization"
          :variant="mode == 'combat' ? 'destructive' : 'default'"
          class="mt-3 px-3 py-1 text-[0.65rem] tracking-[0.15em] uppercase"
        >
          {{ specialization }}
        </Badge>
      </div>
    </div>

    <div class="flex gap-2">
      <Button
        :variant="mode === 'exploration' ? 'default' : 'outline'"
        size="lg"
        class="uppercase tracking-wider"
        @click="mode = 'exploration'"
      >
        <Compass />
        Esplorazione
      </Button>
      <Button
        :variant="mode === 'combat' ? 'destructive' : 'outline'"
        size="lg"
        class="uppercase tracking-wider"
        @click="mode = 'combat'"
      >
        <Swords />
        Combattimento
      </Button>
    </div>
  </header>
</template>
