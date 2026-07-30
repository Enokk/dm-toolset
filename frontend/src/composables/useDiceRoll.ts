import { toast } from 'vue-sonner'

import DiceRollToast from '@/components/character/DiceRollToast.vue'

export function useDiceRoll() {
  function rollDie(sides: number, title: string, modifier = 0) {
    const roll = Math.floor(Math.random() * sides) + 1
    const total = roll + modifier

    toast.custom(DiceRollToast, {
      componentProps: { title, sides, roll, modifier, total },
    })
  }

  function rollD4(title: string, modifier = 0) {
    rollDie(4, title, modifier)
  }

  function rollD6(title: string, modifier = 0) {
    rollDie(6, title, modifier)
  }

  function rollD8(title: string, modifier = 0) {
    rollDie(8, title, modifier)
  }

  function rollD10(title: string, modifier = 0) {
    rollDie(10, title, modifier)
  }

  function rollD12(title: string, modifier = 0) {
    rollDie(12, title, modifier)
  }

  function rollD20(title: string, modifier = 0) {
    rollDie(20, title, modifier)
  }

  function rollD100(title: string, modifier = 0) {
    rollDie(100, title, modifier)
  }

  return { rollD4, rollD6, rollD8, rollD10, rollD12, rollD20, rollD100 }
}
