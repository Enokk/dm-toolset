<script setup lang="ts">
import { Dices } from '@lucide/vue'
import { computed } from 'vue'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useDiceRoll } from '@/composables/useDiceRoll'
import { abilityModifier, formatModifier } from '@/lib/dnd'

const props = defineProps<{
  strength: number
  dexterity: number
  constitution: number
  intelligence: number
  wisdom: number
  charisma: number
}>()

const abilities = computed(() => [
  { key: 'strength', label: 'Forza', abbr: 'FOR', score: props.strength },
  { key: 'dexterity', label: 'Destrezza', abbr: 'DES', score: props.dexterity },
  { key: 'constitution', label: 'Costituzione', abbr: 'COS', score: props.constitution },
  { key: 'intelligence', label: 'Intelligenza', abbr: 'INT', score: props.intelligence },
  { key: 'wisdom', label: 'Saggezza', abbr: 'SAG', score: props.wisdom },
  { key: 'charisma', label: 'Carisma', abbr: 'CAR', score: props.charisma },
])

const abilityColumns = computed(() => [abilities.value.slice(0, 3), abilities.value.slice(3, 6)])

const { rollD20 } = useDiceRoll()

function rollCheck(ability: { label: string, score: number }) {
  rollD20(`Prova di ${ability.label}`, abilityModifier(ability.score))
}
</script>

<template>
  <Card class="p-0">
    <CardContent class="grid grid-cols-2 divide-x divide-border p-2">
      <div
        v-for="(column, index) in abilityColumns"
        :key="index"
        class="grid grid-rows-3 divide-y divide-border"
      >
        <div
          v-for="ability in column"
          :key="ability.key"
          class="flex items-center justify-center gap-4 p-0"
        >
          <div class="flex flex-col items-center gap-1 p-2 pb-3 pr-0">
            <div class="font-medium uppercase tracking-[0.15em] text-muted-foreground">
              {{ ability.abbr }}
            </div>
            <Badge variant="outline">
              {{ ability.score }}
            </Badge>
          </div>
          <span class="text-2xl font-bold">{{ formatModifier(abilityModifier(ability.score)) }}</span>
          <Button
            variant="ghost"
            size="icon"
            :aria-label="`Tira per ${ability.label}`"
            @click="rollCheck(ability)"
          >
            <Dices class="size-5 text-primary" />
          </Button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
