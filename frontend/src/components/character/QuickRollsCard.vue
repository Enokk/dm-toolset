<script setup lang="ts">
import { ChevronLeft, ChevronRight, Dices } from '@lucide/vue'
import { computed, ref } from 'vue'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useDiceRoll } from '@/composables/useDiceRoll'

const DICE_SIDES = [4, 6, 8, 10, 12, 20, 100] as const

const { rollD4, rollD6, rollD8, rollD10, rollD12, rollD20, rollD100 } = useDiceRoll()

const rollers: Record<number, (title: string) => void> = {
  4: rollD4,
  6: rollD6,
  8: rollD8,
  10: rollD10,
  12: rollD12,
  20: rollD20,
  100: rollD100,
}

const diceIndex = ref(DICE_SIDES.indexOf(20))
const sides = computed(() => DICE_SIDES[diceIndex.value] ?? 20)

function previousDie() {
  diceIndex.value = (diceIndex.value - 1 + DICE_SIDES.length) % DICE_SIDES.length
}

function nextDie() {
  diceIndex.value = (diceIndex.value + 1) % DICE_SIDES.length
}

function roll() {
  rollers[sides.value]!('Tiro Rapido')
}
</script>

<template>
  <Card class="p-0">
    <CardContent class="flex flex-col justify-between h-full items-center py-4 text-center">
      <div class="label-caps text-muted-foreground">Tira Dado</div>
      <div class="flex items-center gap-1">
        <Button variant="ghost" size="icon-sm" @click="previousDie">
          <ChevronLeft class="size-4" />
        </Button>
        <span class="text-2xl font-bold w-16">D{{ sides }}</span>
        <Button variant="ghost" size="icon-sm" @click="nextDie">
          <ChevronRight class="size-4" />
        </Button>
      </div>
      <Button variant="ghost" size="icon" @click="roll">
        <Dices class="size-5 text-primary" />
      </Button>
    </CardContent>
  </Card>
</template>
