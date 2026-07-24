<script setup lang="ts">
import { Dices } from '@lucide/vue'
import { computed } from 'vue'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useDiceRoll } from '@/composables/useDiceRoll'
import { abilityModifier, formatModifier } from '@/lib/dnd'

const props = defineProps<{
  dexterity: number
  mode: 'exploration' | 'combat'
}>()

const modifier = computed(() => abilityModifier(props.dexterity))

const { rollD20 } = useDiceRoll()

function roll() {
  rollD20('Iniziativa', modifier.value)
}
</script>

<template>
  <Card :class="['p-0',
      mode === 'combat' ? 'border border-destructive' : 'border border-card']
    ">
    <CardContent class="flex flex-col justify-between h-full items-center py-4 text-center">
      <div class="label-caps text-muted-foreground">Iniziativa</div>
      <span class="text-3xl font-bold">{{ formatModifier(modifier) }}</span>
      <Button variant="ghost" size="icon" @click="roll">
        <Dices :class="['size-5', mode === 'combat' ? 'text-destructive' : 'text-primary']" />
      </Button>
    </CardContent>
  </Card>
</template>
