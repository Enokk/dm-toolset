export function abilityModifier(score: number) {
  return Math.floor((score - 10) / 2)
}

export function formatModifier(modifier: number) {
  return modifier >= 0 ? `+${modifier}` : `${modifier}`
}

export function proficiencyBonusForLevel(level: number) {
  return Math.floor((level - 1) / 4) + 2
}
