import createClient from 'openapi-fetch'

import type { paths } from './schema.d.ts'

// baseUrl left empty: requests go to same-origin `/api/...`, proxied to the
// backend by Vite in dev (see vite.config.ts) and by the reverse proxy in prod.
export const apiClient = createClient<paths>({ baseUrl: '' })
