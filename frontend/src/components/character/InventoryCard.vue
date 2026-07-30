<script setup lang="ts">
import { Backpack, Minus, Plus, Shield, Swords, Wand } from '@lucide/vue'
import { ref } from 'vue'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { type InventoryItem, type InventoryItemCreate, useInventory } from '@/composables/useInventory'
import CurrencyTracker from './CurrencyTracker.vue'
import ItemFormDialog from './ItemFormDialog.vue'

const props = defineProps<{
  characterId: number
  copperPieces: number
  silverPieces: number
  goldPieces: number
  platinumPieces: number
}>()

const emit = defineEmits<{
  changeCurrency: [payload: { copper_pieces: number, silver_pieces: number, gold_pieces: number, platinum_pieces: number }]
}>()

const { items, addItem, updateItem, removeItem } = useInventory(props.characterId)

const dialogOpen = ref(false)
const editingItem = ref<InventoryItem | null>(null)

function openCreateDialog() {
  editingItem.value = null
  dialogOpen.value = true
}

function openEditDialog(item: InventoryItem) {
  editingItem.value = item
  dialogOpen.value = true
}

async function handleSubmit(payload: InventoryItemCreate) {
  if (editingItem.value) {
    await updateItem(editingItem.value.id, payload)
  } else {
    await addItem(payload)
  }
  dialogOpen.value = false
}

async function handleDelete(item: InventoryItem) {
  await removeItem(item.id)
  dialogOpen.value = false
}
</script>

<template>
  <Card class="p-0">
    <CardHeader class="border-b px-4 py-3">
      <CardTitle class="flex items-center gap-4 text-sm label-caps font-bold text-primary">
        <Minus />
        Equipaggiamento
        <Button variant="ghost" size="icon-sm" class="ml-auto" @click="openCreateDialog">
          <Plus class="size-6" />
        </Button>
      </CardTitle>
    </CardHeader>
    <CardContent class="space-y-4">
      <CurrencyTracker
        :copper-pieces="copperPieces"
        :silver-pieces="silverPieces"
        :gold-pieces="goldPieces"
        :platinum-pieces="platinumPieces"
        @change="emit('changeCurrency', $event)"
      />
      <div>
        <div
          v-for="item in items"
          :key="item.id"
          class="flex items-center gap-3 border-t h-8"
        >

          <div class="flex flex-1 min-w-0 items-baseline">
            <span class="label-caps truncate cursor-pointer" @click="openEditDialog(item)">{{ item.name }}</span>
            <span v-if="item.subtitle" class="truncate text-xs text-muted-foreground">— {{ item.subtitle }}</span>
          </div>

          <span v-if="item.type === 'consumable'" class="shrink-0 label-caps text-muted-foreground">×{{ item.quantity }}</span>
          <Swords v-else-if="item.type === 'weapon'" class="shrink-0 size-4 text-muted-foreground" />
          <Shield v-else-if="item.type === 'armor'" class="shrink-0 size-4 text-muted-foreground" />
          <Wand v-else-if="item.type === 'magic'" class="shrink-0 size-4 text-muted-foreground" />
          <Backpack v-else-if="item.type === 'other'" class="shrink-0 size-4 text-muted-foreground" />
        </div>

        <div v-if="items.length === 0" class="flex items-center border-t h-8 label-caps p-8">
          Nessun oggetto nell'inventario.
        </div>
      </div>
    </CardContent>
  </Card>

  <ItemFormDialog
    v-model:open="dialogOpen"
    :item="editingItem"
    @submit="handleSubmit"
    @delete="handleDelete"
  />
</template>
