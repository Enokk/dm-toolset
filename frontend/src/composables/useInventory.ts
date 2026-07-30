import { ref } from 'vue'

import { apiClient } from '@/api/client'
import type { components } from '@/api/schema.d.ts'

export type InventoryItem = components['schemas']['InventoryItemPublic']
export type InventoryItemCreate = components['schemas']['InventoryItemCreate']
export type InventoryItemUpdate = components['schemas']['InventoryItemUpdate']

export const ITEM_TYPES = [
  { value: 'weapon', label: 'Arma' },
  { value: 'armor', label: 'Armatura o Scudo' },
  { value: 'consumable', label: 'Consumabile' },
  { value: 'magic', label: 'Oggetto Magico' },
  { value: 'other', label: 'Altro' },
] as const

export function useInventory(characterId: number) {
  const items = ref<InventoryItem[]>([])

  async function fetch() {
    const { data } = await apiClient.GET('/api/characters/{character_id}/inventory/', {
      params: { path: { character_id: characterId } },
    })
    items.value = data ?? []
  }

  async function addItem(payload: InventoryItemCreate) {
    const { data } = await apiClient.POST('/api/characters/{character_id}/inventory/', {
      params: { path: { character_id: characterId } },
      body: payload,
    })
    if (data) items.value.push(data)
  }

  async function updateItem(itemId: number, payload: InventoryItemUpdate) {
    const { data } = await apiClient.PATCH('/api/characters/{character_id}/inventory/{item_id}', {
      params: { path: { character_id: characterId, item_id: itemId } },
      body: payload,
    })
    if (!data) return

    const index = items.value.findIndex(item => item.id === itemId)
    if (index !== -1) items.value[index] = data
  }

  async function removeItem(itemId: number) {
    const { error } = await apiClient.DELETE('/api/characters/{character_id}/inventory/{item_id}', {
      params: { path: { character_id: characterId, item_id: itemId } },
    })
    if (error) return

    items.value = items.value.filter(item => item.id !== itemId)
  }

  fetch()

  return { items, addItem, updateItem, removeItem }
}
