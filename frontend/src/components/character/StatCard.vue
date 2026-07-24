<script setup lang="ts">
import { Card, CardContent } from '@/components/ui/card'

defineProps<{
  label: string
  value: string | number
  subtitle?: string
}>()
</script>

<template>
  <Card class="p-0">
    <CardContent class="flex flex-col justify-between h-full items-center py-4 text-center">
      <div class="label-caps text-muted-foreground">{{ label }}</div>
      <span class="text-3xl font-bold">{{ value }}</span>
      <div v-if="subtitle" class="label-caps text-muted-foreground">{{ subtitle }}</div>
      <div v-else class="h-0.5" />
    </CardContent>
  </Card>
</template>
