export type AbilityKey = 'strength' | 'dexterity' | 'constitution' | 'intelligence' | 'wisdom' | 'charisma'

export const ABILITY_ABBR: Record<AbilityKey, string> = {
  strength: 'FOR',
  dexterity: 'DES',
  constitution: 'COS',
  intelligence: 'INT',
  wisdom: 'SAG',
  charisma: 'CAR',
}

export function abilityModifier(score: number) {
  return Math.floor((score - 10) / 2)
}

export function formatModifier(modifier: number) {
  return modifier >= 0 ? `+${modifier}` : `${modifier}`
}

export function proficiencyBonusForLevel(level: number) {
  return Math.floor((level - 1) / 4) + 2
}

export function passivePerception(wisdom: number, proficiencyBonus: number, isProficient: boolean) {
  return 10 + abilityModifier(wisdom) + (isProficient ? proficiencyBonus : 0)
}
