<script setup lang="ts">
import { Minus, Plus } from '@lucide/vue'
import { reactive, ref, watch } from 'vue'

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { ITEM_TYPES, type InventoryItem, type InventoryItemCreate } from '@/composables/useInventory'

const props = defineProps<{
  open: boolean
  item: InventoryItem | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'submit': [payload: InventoryItemCreate]
  'delete': [item: InventoryItem]
}>()

interface FormState {
  name: string
  type: string
  subtitle: string
  quantity: number
  is_equippable: boolean
  is_equipped: boolean
  equip_slot: string
}

function emptyForm(): FormState {
  return {
    name: '',
    type: 'other',
    subtitle: '',
    quantity: 1,
    is_equippable: false,
    is_equipped: false,
    equip_slot: '',
  }
}

const form = reactive<FormState>(emptyForm())

const nameError = ref(false)
const slotError = ref(false)

function validateName(): boolean {
  nameError.value = !form.name.trim()
  return !nameError.value
}

function validateSlot(): boolean {
  slotError.value = form.is_equippable && !form.equip_slot.trim()
  return !slotError.value
}

function handleNameInput() {
  if (nameError.value) validateName()
}

function handleSlotInput() {
  if (slotError.value) validateSlot()
}

watch(() => form.is_equippable, (isEquippable) => {
  if (!isEquippable) slotError.value = false
})

function decrementQuantity() {
  form.quantity = Math.max(1, form.quantity - 1)
}

function incrementQuantity() {
  form.quantity += 1
}

watch(() => props.open, (isOpen) => {
  if (!isOpen) return
  Object.assign(form, props.item
    ? { ...emptyForm(), ...props.item, subtitle: props.item.subtitle ?? '', equip_slot: props.item.equip_slot ?? '' }
    : emptyForm())

  nameError.value = false
  slotError.value = false
})

function handleSubmit() {
  const nameValid = validateName()
  const slotValid = validateSlot()
  if (!nameValid || !slotValid) return

  emit('submit', {
    ...form,
    name: form.name.trim(),
    subtitle: form.subtitle.trim() || null,
    equip_slot: form.is_equippable ? (form.equip_slot.trim() || null) : null,
    properties: props.item?.properties ?? {},
  })
}

const deleteConfirmOpen = ref(false)

function handleDelete() {
  if (props.item) emit('delete', props.item)
  deleteConfirmOpen.value = false
}
</script>

<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogContent class="min-w-md" :show-close-button="false">
      <DialogHeader class="border-b px-3 pb-3">
        <DialogTitle class="label-caps font-bold text-primary">
          {{ item ? 'Modifica oggetto' : 'Aggiungi oggetto' }}
        </DialogTitle>
      </DialogHeader>

      <form class="space-y-6" novalidate @submit.prevent="handleSubmit">
        <div class="space-y-2">
          <Label for="item-name" class="label-caps text-muted-foreground">Nome</Label>
          <Input
            id="item-name"
            v-model="form.name"
            class="label-caps"
            :aria-invalid="!!nameError"
            @input="handleNameInput"
          />
        </div>

        <div class="space-y-2">
          <Label for="item-subtitle" class="label-caps text-muted-foreground">Descrizione</Label>
          <Input id="item-subtitle" v-model="form.subtitle" class="label-caps" placeholder="es. lama ancestrale, CA 18..." />
        </div>

        <div class="space-y-2">
          <Label for="item-type" class="label-caps text-muted-foreground">Tipo</Label>
          <Select v-model="form.type">
            <SelectTrigger id="item-type" class="w-full label-caps">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="itemType in ITEM_TYPES" :key="itemType.value" :value="itemType.value" class="label-caps">
                {{ itemType.label }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div class="flex justify-between h-7">
          <div class="flex items-center gap-4">
            <Switch id="item-equippable" v-model="form.is_equippable" />
            <Label for="item-equippable" class="label-caps text-muted-foreground">Equipaggiabile</Label>
          </div>

          <div v-if="form.type === 'consumable'" class="flex items-center gap-1">
            <Label for="item-quantity" class="pr-2 label-caps text-muted-foreground">Quantità</Label>
            <Input
              id="item-quantity"
              v-model.number="form.quantity"
              type="number"
              min="1"
              class="w-12 [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
            />
            <Button type="button" variant="outline" size="icon" @click="decrementQuantity">
              <Minus />
            </Button>
            <Button type="button" variant="outline" size="icon" @click="incrementQuantity">
              <Plus />
            </Button>
          </div>
        </div>

        <div v-if="form.is_equippable" class="space-y-2">
          <Label for="item-slot" class="label-caps text-muted-foreground">Slot</Label>
          <Input
            id="item-slot"
            v-model="form.equip_slot"
            class="label-caps"
            placeholder="es. arma, scudo, armatura..."
            :aria-invalid="!!slotError"
            @input="handleSlotInput"
          />
        </div>

        <DialogFooter class="border-t pt-4">
          <Button
            v-if="item"
            type="button"
            variant="destructive"
            class="w-25 label-caps mr-auto"
            @click="deleteConfirmOpen = true"
          >
            Elimina
          </Button>
          <Button type="button" variant="outline" class="w-25 label-caps" @click="emit('update:open', false)">
            Annulla
          </Button>
          <Button type="submit" class="w-25 label-caps">
            {{ item ? 'Salva' : 'Aggiungi' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>

  <AlertDialog v-model:open="deleteConfirmOpen">
    <AlertDialogContent>
      <AlertDialogHeader class="border-b pb-3">
        <AlertDialogTitle class="flex items-center gap-4 text-sm label-caps font-bold text-destructive">
          Eliminare l'oggetto?
        </AlertDialogTitle>
        <AlertDialogDescription class="pt-2 label-caps">
          "{{ item?.name }}" verrà rimosso dall'inventario. L'azione non può essere annullata.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="w-25 label-caps">
          Annulla
        </AlertDialogCancel>
        <AlertDialogAction
          class="w-25 label-caps bg-destructive/20 text-destructive hover:bg-destructive/30"
          @click="handleDelete"
        >
          Elimina
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
