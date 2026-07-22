import { ref } from 'vue'

import { apiClient } from '@/api/client'
import type { components } from '@/api/schema.d.ts'

type Character = components['schemas']['CharacterPublic']

export function useCharacter(characterId: number) {
  const character = ref<Character | null>(null)
  const notFound = ref(false)

  async function fetch() {
    const { data, error } = await apiClient.GET('/api/characters/{character_id}', {
      params: { path: { character_id: characterId } },
    })
    character.value = data ?? null
    notFound.value = !!error
  }

  async function updateVitals({ current, temp }: { current: number, temp: number }) {
    if (!character.value) return

    const { data } = await apiClient.PATCH('/api/characters/{character_id}/vitals', {
      params: { path: { character_id: character.value.id } },
      body: { hit_points_current: current, hit_points_temp: temp },
    })

    if (data) character.value = data
  }

  fetch()

  return { character, notFound, updateVitals }
}
