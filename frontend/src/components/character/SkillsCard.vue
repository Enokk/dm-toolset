<script setup lang="ts">
import { Dices, Minus } from '@lucide/vue'
import { computed } from 'vue'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useDiceRoll } from '@/composables/useDiceRoll'
import { ABILITY_ABBR, type AbilityKey, abilityModifier, formatModifier } from '@/lib/dnd'

export type SkillKey =
  | 'acrobatics'
  | 'animalHandling'
  | 'arcana'
  | 'athletics'
  | 'deception'
  | 'history'
  | 'insight'
  | 'intimidation'
  | 'investigation'
  | 'medicine'
  | 'nature'
  | 'perception'
  | 'performance'
  | 'persuasion'
  | 'religion'
  | 'sleightOfHand'
  | 'stealth'
  | 'survival'

const props = defineProps<{
  strength: number
  dexterity: number
  constitution: number
  intelligence: number
  wisdom: number
  charisma: number
  proficiencyBonus: number
  proficientIn: SkillKey[]
  mode: 'exploration' | 'combat'
}>()

const SKILL_DEFINITIONS: { key: SkillKey, label: string, ability: AbilityKey }[] = [
  { key: 'acrobatics', label: 'Acrobazia', ability: 'dexterity' },
  { key: 'animalHandling', label: 'Addestrare Animali', ability: 'wisdom' },
  { key: 'arcana', label: 'Arcano', ability: 'intelligence' },
  { key: 'athletics', label: 'Atletica', ability: 'strength' },
  { key: 'deception', label: 'Inganno', ability: 'charisma' },
  { key: 'history', label: 'Storia', ability: 'intelligence' },
  { key: 'insight', label: 'Intuizione', ability: 'wisdom' },
  { key: 'intimidation', label: 'Intimidire', ability: 'charisma' },
  { key: 'investigation', label: 'Indagare', ability: 'intelligence' },
  { key: 'medicine', label: 'Medicina', ability: 'wisdom' },
  { key: 'nature', label: 'Natura', ability: 'intelligence' },
  { key: 'perception', label: 'Percezione', ability: 'wisdom' },
  { key: 'performance', label: 'Intrattenere', ability: 'charisma' },
  { key: 'persuasion', label: 'Persuasione', ability: 'charisma' },
  { key: 'religion', label: 'Religione', ability: 'intelligence' },
  { key: 'sleightOfHand', label: 'Rapidità di Mano', ability: 'dexterity' },
  { key: 'stealth', label: 'Furtività', ability: 'dexterity' },
  { key: 'survival', label: 'Sopravvivenza', ability: 'wisdom' },
]

const abilityScores: Record<AbilityKey, number> = {
  strength: props.strength,
  dexterity: props.dexterity,
  constitution: props.constitution,
  intelligence: props.intelligence,
  wisdom: props.wisdom,
  charisma: props.charisma,
}

const skills = computed(() => {
  return [...SKILL_DEFINITIONS]
    .sort((a, b) => a.label.localeCompare(b.label, 'it'))
    .map((skill) => {
      const proficient = props.proficientIn.includes(skill.key)
      const modifier = abilityModifier(abilityScores[skill.ability]) + (proficient ? props.proficiencyBonus : 0)
      return { ...skill, proficient, modifier }
    })
})

const { rollD20 } = useDiceRoll()

function rollSkill(skill: { label: string, modifier: number }) {
  rollD20(`Prova di ${skill.label}`, skill.modifier)
}
</script>

<template>
  <Card class="p-0">
    <CardHeader class="border-b px-4 py-3">
      <CardTitle :class="[
          'flex items-center gap-4 text-sm label-caps font-bold',
          props.mode === 'combat' ? 'text-destructive' : 'text-primary'
        ]">
        <Minus />
        Abilità
      </CardTitle>
    </CardHeader>
    <CardContent class="space-y-2 p-4 pt-0">
      <div
        v-for="skill in skills"
        :key="skill.key"
        class="flex items-center gap-3"
      >
        <span
          :class="[
            'size-2.5 shrink-0 rounded-full border',
            mode === 'combat' ? 'border-destructive' : 'border-primary',
            skill.proficient ? (mode === 'combat' ? 'bg-destructive' : 'bg-primary') : 'bg-transparent',
          ]"
        />
        <span
          :class="[
            'text-xs label-caps',
            skill.proficient ? 'font-semibold text-foreground' : 'text-muted-foreground',
          ]"
        >
          {{ skill.label }}
        </span>
        <span class="ml-auto mr-8 text-xs label-caps text-muted-foreground">{{ ABILITY_ABBR[skill.ability] }}</span>
        <span class="mr-8 text-right text-base font-semibold">{{ formatModifier(skill.modifier) }}</span>
        <Button
          variant="ghost"
          size="icon"
          class="mr-3"
          @click="rollSkill(skill)"
        >
          <Dices :class="['size-5', mode === 'combat' ? 'text-destructive' : 'text-primary']" />
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
