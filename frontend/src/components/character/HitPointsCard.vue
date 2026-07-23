<script setup lang="ts">
import { Heart } from '@lucide/vue'
import { computed } from 'vue'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ButtonGroup } from '@/components/ui/button-group'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

const props = defineProps<{
  current: number
  max: number
  temp: number
}>()

const emit = defineEmits<{
  change: [payload: { current: number, temp: number }]
}>()

const barPercent = computed(() => (props.current / props.max) * 100)

const barIndicatorClass = computed(() => {
  if (barPercent.value > 67) return '[&>[data-slot=progress-indicator]]:bg-success'
  if (barPercent.value < 33) return '[&>[data-slot=progress-indicator]]:bg-destructive'
  return '[&>[data-slot=progress-indicator]]:bg-primary'
})

function applyDamage(amount: number) {
  let temp = props.temp
  let remaining = amount

  if (temp > 0) {
    const absorbed = Math.min(temp, remaining)
    temp -= absorbed
    remaining -= absorbed
  }

  const current = Math.max(0, props.current - remaining)
  emit('change', { current, temp })
}

function applyHeal(amount: number) {
  const current = Math.min(props.max, props.current + amount)
  emit('change', { current, temp: props.temp })
}

function addTemp() {
  emit('change', { current: props.current, temp: props.temp + 5 })
}
</script>

<template>
  <Card>
    <CardContent class="space-y-3">
      <div class="flex items-baseline gap-1.5">
        <Heart class="ml-2 size-6 text-muted-foreground" />
        <span class="ml-1 text-3xl font-bold">{{ current }}</span>
        <span class="text-sm text-muted-foreground">/ {{ max }}</span>
        <Badge v-if="temp > 0" variant="outline" class="ml-auto text-success">
          +{{ temp }} temp
        </Badge>
      </div>

      <Progress :model-value="barPercent" :class="['h-1.5', barIndicatorClass]" />

      <ButtonGroup class="w-[60%]">
        <Button variant="secondary" size="sm" @click="applyDamage(5)" class="flex-1 text-destructive">
          -5
        </Button>
        <Button variant="secondary" size="sm" @click="applyDamage(1)" class="flex-1 text-destructive">
          -1
        </Button>
        <Button variant="secondary" size="sm" @click="applyHeal(1)" class="flex-1 text-success">
          +1
        </Button>
        <Button variant="secondary" size="sm" @click="applyHeal(5)" class="flex-1 text-success">
          +5
        </Button>
        <Button variant="secondary" size="sm" @click="addTemp" class="flex-1">
          +Temp
        </Button>
      </ButtonGroup>
    </CardContent>
  </Card>
</template>
