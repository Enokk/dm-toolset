<script setup lang="ts">
import { Minus, Shield, Swords } from '@lucide/vue'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { components } from '@/api/schema.d.ts'

type ProficiencyEntry = components['schemas']['ProficiencyEntry']

defineProps<{
  weapons: ProficiencyEntry[]
  armor: ProficiencyEntry[]
  mode: 'exploration' | 'combat'
}>()

const SOURCE_LABEL: Record<ProficiencyEntry['source'], string> = {
  race: 'Razza',
  class: 'Classe',
  subclass: 'Sottoclasse',
}
</script>

<template>
  <Card class="p-0">
    <CardHeader class="border-b px-4 py-3">
      <CardTitle :class="[
          'flex items-center gap-4 text-sm label-caps font-bold',
          mode === 'combat' ? 'text-destructive' : 'text-primary'
        ]">
        <Minus />
        Competenze
      </CardTitle>
    </CardHeader>
    <CardContent class="space-y-4 p-4 pt-0">
      <div>
        <div class="mb-2 flex gap-2 text-xs label-caps text-muted-foreground">
          <Swords class="size-4" />
          Armi
        </div>
        <p v-if="weapons.length === 0" class="ml-4 text-xs label-caps text-muted-foreground">Nessuna</p>
        <div v-else class="space-y-1.5">
          <div
            v-for="entry in weapons"
            :key="`${entry.source}-${entry.name}`"
            class="flex justify-between"
          >
            <span class="text-xs label-caps text-foreground">{{ entry.name }}</span>
            <span class="text-[10px] label-caps text-muted-foreground">{{ SOURCE_LABEL[entry.source] }}</span>
          </div>
        </div>
      </div>

      <div>
        <div class="mb-2 flex gap-2 text-xs label-caps text-muted-foreground">
          <Shield class="size-4" />
          Armature
        </div>
        <p v-if="armor.length === 0" class="text-xs label-caps text-muted-foreground">Nessuna</p>
        <div v-else class="space-y-1.5">
          <div
            v-for="entry in armor"
            :key="`${entry.source}-${entry.name}`"
            class="flex justify-between"
          >
            <span class="text-xs label-caps text-foreground">{{ entry.name }}</span>
            <span class="text-[10px] label-caps text-muted-foreground">{{ SOURCE_LABEL[entry.source] }}</span>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
