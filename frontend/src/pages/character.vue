<script setup lang="ts">
import { ref } from 'vue'

import AbilityScoresCard from '@/components/character/AbilityScoresCard.vue'
import CharacterHeader from '@/components/character/CharacterHeader.vue'
import HitPointsCard from '@/components/character/HitPointsCard.vue'
import InitiativeCard from '@/components/character/InitiativeCard.vue'
import InventoryCard from '@/components/character/InventoryCard.vue'
import QuickRollsCard from '@/components/character/QuickRollsCard.vue'
import SavingThrowsCard from '@/components/character/SavingThrowsCard.vue'
import SkillsCard from '@/components/character/SkillsCard.vue'
import StatCard from '@/components/character/StatCard.vue'
import { useCharacter } from '@/composables/useCharacter'
import { formatModifier, passivePerception, proficiencyBonusForLevel } from '@/lib/dnd'

const mode = ref<'exploration' | 'combat'>('exploration')

const { character, notFound, updateVitals, updateCurrency } = useCharacter(1)

// Placeholder until class/talent-driven proficiency is modeled on the backend.
const savingThrowProficiencies = ['strength', 'constitution'] as const
const skillProficiencies = ['animalHandling', 'athletics', 'perception', 'survival'] as const
</script>

<template>
  <div class="mx-auto w-350 pt-8">
    <div v-if="character" class="rounded-lg border">
      <div class="border-b bg-linear-to-b from-muted to-background px-10 pt-8">
        <CharacterHeader
          v-model:mode="mode"
          :name="character.name"
          :character-race="character.character_race.name"
          :character-class="character.character_class.name"
          :level="character.level"
        />
      </div>

      <main class="px-10 py-8">
        <div class="grid grid-cols-10 gap-4">
          <HitPointsCard
            :current="character.hit_points_current"
            :max="character.hit_points_max"
            :temp="character.hit_points_temp"
            class="col-span-4"
            @change="updateVitals"
          />
          <StatCard
            label="Classe Armatura"
            :value="'##'"
            class="col-span-1"
          />
          <InitiativeCard
            :dexterity="character.dexterity"
            :mode="mode"
            class="col-span-1"
          />
          <StatCard
            label="Velocità"
            :value="character.character_race.speed"
            subtitle="metri"
            class="col-span-1"
          />
          <StatCard
            label="Bonus di Competenza"
            :value="formatModifier(proficiencyBonusForLevel(character.level))"
            class="col-span-1"
          />
          <StatCard
            label="Percezione Passiva"
            :value="passivePerception(character.wisdom, proficiencyBonusForLevel(character.level), skillProficiencies.includes('perception'))"
            class="col-span-1"
          />
          <QuickRollsCard class="col-span-1" />
        </div>

        <div class="grid grid-cols-12 gap-4 mt-4">
          <div class="col-span-3 flex flex-col gap-4">
            <AbilityScoresCard
              :strength="character.strength"
              :dexterity="character.dexterity"
              :constitution="character.constitution"
              :intelligence="character.intelligence"
              :wisdom="character.wisdom"
              :charisma="character.charisma"
              :mode="mode"
            />
            <SavingThrowsCard
              :strength="character.strength"
              :dexterity="character.dexterity"
              :constitution="character.constitution"
              :intelligence="character.intelligence"
              :wisdom="character.wisdom"
              :charisma="character.charisma"
              :proficiency-bonus="proficiencyBonusForLevel(character.level)"
              :proficient-in="[...savingThrowProficiencies]"
              :mode="mode"
            />
          </div>
          <div class="col-span-4">
            <SkillsCard
              :strength="character.strength"
              :dexterity="character.dexterity"
              :constitution="character.constitution"
              :intelligence="character.intelligence"
              :wisdom="character.wisdom"
              :charisma="character.charisma"
              :proficiency-bonus="proficiencyBonusForLevel(character.level)"
              :proficient-in="[...skillProficiencies]"
              :mode="mode"
            />
          </div>
          <div class="col-span-5" v-if="mode === 'exploration'">
            <InventoryCard
            :character-id="character.id"
            :copper-pieces="character.copper_pieces"
            :silver-pieces="character.silver_pieces"
            :gold-pieces="character.gold_pieces"
            :platinum-pieces="character.platinum_pieces"
            @change-currency="updateCurrency"
            />
          </div>
        </div>
      </main>
    </div>

    <p v-else-if="notFound" class="text-destructive">Personaggio non trovato.</p>
  </div>
</template>
