import { ref } from 'vue'

import { apiClient } from '@/api/client'
import type { components } from '@/api/schema.d.ts'

type ProficienciesPublic = components['schemas']['ProficienciesPublic']

export function useProficiencies(characterId: number) {
  const proficiencies = ref<ProficienciesPublic | null>(null)

  async function fetch() {
    const { data } = await apiClient.GET('/api/characters/{character_id}/proficiencies/', {
      params: { path: { character_id: characterId } },
    })
    proficiencies.value = data ?? null
  }

  fetch()

  return { proficiencies }
}
