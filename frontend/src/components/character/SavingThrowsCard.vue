<script setup lang="ts">
import { Dices, Minus } from '@lucide/vue'
import { computed } from 'vue'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useDiceRoll } from '@/composables/useDiceRoll'
import { abilityModifier, formatModifier } from '@/lib/dnd'

export type AbilityKey = 'strength' | 'dexterity' | 'constitution' | 'intelligence' | 'wisdom' | 'charisma'

const props = defineProps<{
  strength: number
  dexterity: number
  constitution: number
  intelligence: number
  wisdom: number
  charisma: number
  proficiencyBonus: number
  proficientIn: AbilityKey[]
  mode: 'exploration' | 'combat'
}>()

const savingThrows = computed(() => {
  const abilities: { key: AbilityKey, label: string, abbr: string, score: number }[] = [
    { key: 'strength', label: 'Forza', abbr: 'FOR', score: props.strength },
    { key: 'dexterity', label: 'Destrezza', abbr: 'DES', score: props.dexterity },
    { key: 'constitution', label: 'Costituzione', abbr: 'COS', score: props.constitution },
    { key: 'intelligence', label: 'Intelligenza', abbr: 'INT', score: props.intelligence },
    { key: 'wisdom', label: 'Saggezza', abbr: 'SAG', score: props.wisdom },
    { key: 'charisma', label: 'Carisma', abbr: 'CAR', score: props.charisma },
  ]

  return abilities.map((ability) => {
    const proficient = props.proficientIn.includes(ability.key)
    const modifier = abilityModifier(ability.score) + (proficient ? props.proficiencyBonus : 0)
    return { ...ability, proficient, modifier }
  })
})

const { rollD20 } = useDiceRoll()

function rollSave(save: { label: string, modifier: number }) {
  rollD20(`Tiro Salvezza su ${save.label}`, save.modifier)
}
</script>

<template>
  <Card class="p-0">
    <CardHeader class="border-b px-4 py-3">
      <CardTitle class="flex items-center gap-4 text-sm label-caps font-bold">
        <Minus></Minus>
        Tiri Salvezza
      </CardTitle>
    </CardHeader>
    <CardContent class="space-y-3 p-4 pt-0">
      <div
        v-for="save in savingThrows"
        :key="save.key"
        class="flex items-center gap-3"
      >
        <span
          :class="[
            'size-2.5 shrink-0 rounded-full border',
            props.mode === 'combat' ? 'border-destructive' : 'border-primary',
            save.proficient ? (props.mode === 'combat' ? 'bg-destructive' : 'bg-primary') : 'bg-transparent',
          ]"
        />
        <span class="text-xs label-caps text-muted-foreground">
          {{ save.label }}
        </span>
        <span class="ml-auto mr-6 text-base font-semibold">{{ formatModifier(save.modifier) }}</span>
        <Button
          variant="ghost"
          size="icon"
          :aria-label="`Tira Tiro Salvezza su ${save.label}`"
          class="mr-3"
          @click="rollSave(save)"
        >
          <Dices :class="['size-5', props.mode === 'combat' ? 'text-destructive' : 'text-primary']" />
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
