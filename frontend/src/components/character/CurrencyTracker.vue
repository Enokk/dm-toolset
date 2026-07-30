<script setup lang="ts">
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'

import copperIcon from '@/assets/currency/copper.png'
import goldIcon from '@/assets/currency/gold.png'
import platinumIcon from '@/assets/currency/platinum.png'
import silverIcon from '@/assets/currency/silver.png'

const props = defineProps<{
  copperPieces: number
  silverPieces: number
  goldPieces: number
  platinumPieces: number
}>()

const emit = defineEmits<{
  change: [payload: { copper_pieces: number, silver_pieces: number, gold_pieces: number, platinum_pieces: number }]
}>()

type CurrencyField = 'copper_pieces' | 'silver_pieces' | 'gold_pieces' | 'platinum_pieces'

const DENOMINATIONS: { field: CurrencyField, label: string, icon: string }[] = [
  { field: 'platinum_pieces', label: 'Platino', icon: platinumIcon },
  { field: 'gold_pieces', label: 'Oro', icon: goldIcon },
  { field: 'silver_pieces', label: 'Argento', icon: silverIcon },
  { field: 'copper_pieces', label: 'Rame', icon: copperIcon },
]

function valueFor(field: CurrencyField) {
  return {
    copper_pieces: props.copperPieces,
    silver_pieces: props.silverPieces,
    gold_pieces: props.goldPieces,
    platinum_pieces: props.platinumPieces,
  }[field]
}

function onChange(field: CurrencyField, event: Event) {
  const parsed = Math.max(0, Math.trunc(Number((event.target as HTMLInputElement).value)) || 0)
  emit('change', {
    copper_pieces: props.copperPieces,
    silver_pieces: props.silverPieces,
    gold_pieces: props.goldPieces,
    platinum_pieces: props.platinumPieces,
    [field]: parsed,
  })
}
</script>

<template>
  <div class="grid grid-cols-4 gap-2">
    <Card v-for="denom in DENOMINATIONS" :key="denom.field" class="p-0">
      <CardContent class="flex flex-row items-center gap-2 p-2">
        <img :src="denom.icon" :alt="denom.label" class="size-6 shrink-0">
        <Input
          type="number"
          min="0"
          :model-value="valueFor(denom.field)"
          class="w-full label-caps text-center [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
          @change="onChange(denom.field, $event)"
        />
      </CardContent>
    </Card>
  </div>
</template>
