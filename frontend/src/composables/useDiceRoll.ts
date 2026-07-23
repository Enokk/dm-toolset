import { toast } from 'vue-sonner'

import DiceRollToast from '@/components/character/DiceRollToast.vue'

export function useDiceRoll() {
  function rollD20(title: string, modifier: number) {
    const roll = Math.floor(Math.random() * 20) + 1
    const total = roll + modifier

    toast.custom(DiceRollToast, {
      componentProps: { title, roll, modifier, total },
    })
  }

  return { rollD20 }
}
