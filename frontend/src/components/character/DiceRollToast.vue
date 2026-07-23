<script setup lang="ts">
import { computed } from 'vue'

import { Badge } from '@/components/ui/badge'

const props = defineProps<{
  title: string
  roll: number
  modifier: number
  total: number
}>()

const isCritical = computed(() => props.roll === 20)
const isFumble = computed(() => props.roll === 1)

const formula = computed(() => {
  if (props.modifier === 0) return `d20 (${props.roll})`
  const sign = props.modifier > 0 ? '+' : '-'
  return `d20 (${props.roll}) ${sign} ${Math.abs(props.modifier)}`
})
</script>

<template>
  <div
    class="flex w-60 flex-col items-center gap-1 rounded-lg border bg-popover p-4"
    :class="isCritical ? 'border-success' : isFumble ? 'border-destructive' : 'border-border'"
  >
    <span class="text-xs label-caps text-muted-foreground">
      {{ title }}
    </span>
    <span
      class="text-4xl font-bold"
      :class="isCritical ? 'text-success' : isFumble ? 'text-destructive' : 'text-foreground'"
    >
      {{ total }}
    </span>
    <span class="font-mono text-sm text-muted-foreground">
      {{ formula }}
    </span>
    <Badge
      v-if="isCritical || isFumble"
      variant="secondary"
      class="mt-1 label-caps"
      :class="isCritical ? 'text-success' : 'text-destructive'"
    >
      {{ isCritical ? 'Successo critico' : 'Fallimento critico' }}
    </Badge>
  </div>
</template>
