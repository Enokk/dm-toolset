# DM Toolset — Decisioni Architetturali

Documento di riferimento per le scelte architetturali del progetto. Serve sia come guida per chi sviluppa sia come contesto persistente per riprendere il progetto in futuro (incluse eventuali sessioni assistite da AI).

## Cos'è il progetto

Web app che parte come sostituto digitale di una scheda personaggio cartacea di D&D 5e, con l'obiettivo di evolvere progressivamente in un tool completo per Dungeon Master: gestione campagne, incontri, ambientazioni, dati di riferimento (mostri, incantesimi, oggetti), ecc.

**Contesto d'uso:** progetto personale/hobbistico, utilizzato da un piccolo gruppo di amici. Non è un prodotto destinato a un pubblico ampio: performance e scalabilità estrema non sono requisiti reali, semplicità e velocità di sviluppo sono la priorità.

## Stack tecnologico

| Layer | Tecnologia |
|---|---|
| Frontend | Vue |
| CSS | Tailwind CSS |
| Componenti UI | shadcn-vue / Reka UI |
| Backend | FastAPI (Python) |
| ORM / modelli | SQLModel |
| Migrazioni DB | Alembic |
| Database | PostgreSQL |

##  Detagli dello stack

### Backend: FastAPI

- Async-first, type hints ovunque, community in forte crescita: è la scelta più moderna per un backend Python nuovo, disaccoppiato da un frontend JS.
- Genera automaticamente documentazione OpenAPI, comoda per lo sviluppo con frontend e backend separati.
- Si integra bene con Pydantic/SQLModel per la validazione dei dati.
- **Attenzione futura:** FastAPI non offre un admin panel pronto all'uso. Se la gestione di dati di reference (mostri, incantesimi, oggetti) diventasse onerosa da mantenere via API/UI custom, valutare strumenti come SQLAdmin o un pannello interno leggero dedicato.

### Frontend: Vue

- Curva di apprendimento dolce, poco boilerplate, ecosistema ufficiale coerente (Vue Router, Pinia) — adatto a un team piccolo che vuole essere produttivo rapidamente.
- Comunica con il backend esclusivamente via API JSON (SPA disaccoppiata da FastAPI), nessun rendering server-side coinvolto.

### Routing frontend: file-based routing con vue-router

- Le rotte **non vengono dichiarate a mano** in un file router: `vue-router` (dalla v5, che ha assorbito il precedente pacchetto separato `unplugin-vue-router`) genera l'array di routes leggendo la struttura di `frontend/src/pages/`, tramite il plugin Vite `vue-router/vite` configurato in `vite.config.ts` (deve stare prima di `@vitejs/plugin-vue` nell'array `plugins`).
- Convenzione: ogni file/cartella in `src/pages` diventa un segmento di path.
  - Path statici e param dinamici:
    ```
    src/pages/
    ├── index.vue                → /
    └── characters/
        ├── index.vue             → /characters
        └── [id].vue               → /characters/:id
    ```
  - Nesting sotto un param dinamico (es. tab della scheda personaggio): il file `[id].vue` diventa il **layout** della rotta (deve contenere un `<router-view />` per renderizzare i figli), e la cartella omonima `[id]/` contiene le sotto-pagine:
    ```
    src/pages/characters/
    ├── [id].vue                  ← layout per /characters/:id/* (ha <router-view />)
    └── [id]/
        ├── index.vue              → /characters/:id
        ├── spells.vue              → /characters/:id/spells
        └── inventory.vue            → /characters/:id/inventory
    ```
  - Varianti sul param: `[[id]].vue` → param opzionale; `[...slug].vue` → catch-all (`/docs/a/b` → `slug: ['a','b']`).
- `frontend/src/router/index.ts` resta solo il punto di assemblaggio: importa `routes` da `vue-router/auto-routes` e crea il router — non va più editato per aggiungere una view, basta creare il file in `src/pages`.
- **Routes tipizzate**: il plugin genera `frontend/typed-router.d.ts` (committato in git, come consigliato dal tool stesso — rigenerato automaticamente ad ogni dev/build, ma serve già presente perché `vue-tsc --build` e `vite build` girano in parallelo nello script `build`). Serve anche `vueCompilerOptions` in `tsconfig.app.json` (plugin Volar `vue-router/volar/sfc-typed-router` + `rootDir`) per avere `useRoute()` tipizzato per-pagina nell'editor.
- **Compromesso accettato:** la struttura delle cartelle *è* la definizione delle rotte — rinominare/spostare un file `.vue` in `pages/` cambia l'URL. Per meta-field per-rotta (titolo, `requiresAuth`, ecc.) si userà la macro `definePage()` nel componente invece di un oggetto route scritto a mano.

### Modelli e migrazioni: SQLModel + Alembic

- **SQLModel** unifica modello DB e schema API in un'unica classe, riducendo il boilerplate tra layer di persistenza e layer di validazione/serializzazione.
- **Alembic** gestisce le migrazioni su Postgres: autogenerate confrontando i modelli con lo stato del DB, supporto upgrade/downgrade. SQLModel non sostituisce Alembic: le migrazioni si fanno comunque con Alembic.

### Accesso al DB: sincrono, non async

- Nonostante FastAPI sia async-first, l'accesso al DB (`engine`/`Session` di SQLModel/SQLAlchemy) resta **sincrono**: nessun `create_async_engine`/`AsyncSession`.
- Le route e le dependency che toccano il DB vanno definite come `def` (non `async def`): FastAPI le esegue automaticamente in un thread pool, evitando di bloccare l'event loop con I/O bloccante.
- Scelta guidata dalla semplicità del progetto: evita un driver Postgres async dedicato (es. `asyncpg`) e la doppia gestione sync/async in SQLModel (Alembic resta comunque sync). Da rivalutare solo se emergono reali esigenze di concorrenza elevata.

### Tipi frontend e client da OpenAPI: openapi-typescript + openapi-fetch

- Lo schema OpenAPI viene esportato in un file statico (`backend/scripts/export_openapi.py`, importa direttamente l'app FastAPI e scrive `openapi.json`, senza bisogno di un server in esecuzione); da questo file **openapi-typescript** genera i tipi TypeScript (`frontend/src/api/schema.d.ts`).
- **openapi-fetch** fornisce anche il client HTTP tipizzato (`frontend/src/api/client.ts`, `createClient<paths>({ baseUrl: '' })`, `baseUrl` vuoto perché le chiamate sono same-origin su `/api/...`, proxate dal dev server Vite e in futuro da un reverse proxy in produzione). **Decisione rivista** rispetto all'impostazione iniziale (client scritto a mano): il client generato riduce il boilerplate sulle singole chiamate senza perdere la tipizzazione end-to-end derivata dai modelli backend.
- Da rilanciare come script (`npm run gen:api`, che concatena `gen:api:schema` + `gen:api:types`) ogni volta che lo schema del backend cambia; non è una sincronizzazione automatica/live.

### Chiamate al backend: composables per dominio

- Ogni dominio applicativo (personaggio, inventario, competenze, in futuro incantesimi, ecc.) espone un composable dedicato in `src/composables/` (es. `useCharacter.ts`, `useInventory.ts`, `useProficiencies.ts`) che incapsula le chiamate ad `apiClient` (il client tipizzato openapi-fetch, vedi sopra) e restituisce stato reattivo (dati, flag come `notFound`) più le azioni disponibili (es. `updateVitals`, `updateCurrency`). I componenti Vue non chiamano mai `apiClient` direttamente.
- Scelta guidata dalla dimensione attuale del progetto: evita di introdurre uno state manager globale (Pinia) o una libreria di server-state (TanStack Query / Vue Query) prima che il problema che risolvono si presenti davvero — approccio incrementale, non "big design up front".
- **Ancora valido** dopo l'aggiunta dei domini inventario/competenze: la pagina personaggio resta un'unica vista che istanzia più composable indipendenti (uno per dominio) sullo stesso `character_id`; nessuno stato è condiviso tra viste sorelle, quindi i trigger sotto non sono ancora scattati.
- **Trigger per introdurre Pinia** (già presente tra le dipendenze ma non ancora usata): quando uno stato deve essere condiviso tra componenti che non sono in relazione padre/figlio (es. un header globale col personaggio attivo, visibile insieme alle sotto-pagine inventario/incantesimi). Finché i dati restano confinati a una vista e alle sue sotto-viste dirette, route param + composable locale bastano.
- **Trigger per introdurre TanStack Query (Vue Query)**: quando una mutation in un dominio deve invalidare/aggiornare dati letti da un altro dominio (es. equipaggiare un'arma nell'inventario che deve riflettersi su CA/peso mostrati nella scheda personaggio), o quando serve caching/deduplica reale tra viste diverse.

### CSS e componenti UI: Tailwind + shadcn-vue/Reka UI

- **Tailwind CSS** per lo styling: utility-first, nessun foglio di stile separato da mantenere in parallelo ai componenti.
- Per i widget (dialog, dropdown, tabs, tooltip, ecc.) si è scelto un approccio **headless** invece di una libreria "tutto incluso" (es. PrimeVue, Vuetify): **Reka UI** fornisce i componenti primitivi (comportamento, accessibilità, gestione focus/tastiera/ARIA) senza alcuno stile imposto; **shadcn-vue** è la libreria di componenti pre-costruiti sopra Reka UI, distribuita come codice da copiare nel progetto (non un package da installare) così che lo stile Tailwind applicato sia interamente personalizzabile.
- Scelta guidata dalla volontà di un design totalmente personalizzabile, senza il "look" riconoscibile delle librerie tutto-incluso e senza rischio di funzionalità premium a pagamento.
- **Compromesso accettato:** per componenti complessi come tabelle con sort/filtri/paginazione non c'è un widget già pronto: va usata una libreria headless dedicata (es. **TanStack Table**) per la logica, con markup e stile scritti a mano. Richiede più lavoro iniziale rispetto a un kit all-in-one.
- **Notifiche/toast: vue-sonner**, montato una sola volta in `App.vue` (`<Toaster />`, sopra il `<RouterView />`, così è disponibile globalmente). Usato per il feedback immediato dei tiri di dado (`useDiceRoll.ts` chiama `toast.custom(...)` con un componente `DiceRollToast.vue` dedicato) — coerente con la scelta headless-per-lo-stile fatta per il resto della UI.

### Struttura repo e tooling

- **Monorepo**: un solo repository Git con `/backend` e `/frontend` come cartelle separate a livello di root.
- **Backend**: gestito con **uv** (package manager Python moderno, veloce, gestisce venv/dipendenze/lockfile in un comando).
- **Frontend**: gestito con **pnpm** (via corepack).
- **Postgres in locale**: nessun container dedicato per ora — si usa un'istanza Postgres già presente in locale (porta 5432). La containerizzazione (Postgres incluso) è rimandata alla fase di distribuzione del progetto.
- **Lingua di codice/log**: codice, identificatori, docstring e messaggi di log/errore in **inglese** (convenzione standard, compatibile con strumenti/librerie che leggono i log); i commenti tecnici possono restare in italiano. La documentazione di progetto (questo file) resta in italiano. Non va confusa con la localizzazione IT/EN vista sopra, che riguarda il contenuto mostrato all'utente finale, non il codice.

## Note per contesti futuri

- Scaffold iniziale completato: backend FastAPI (`/backend`, struttura `src/dm_toolset_backend` con `core/config.py`, `core/db.py`, `api/`, `models/`) e frontend Vue (`/frontend`, Vite + TS + Router (file-based, vedi sopra) + Pinia + Tailwind + shadcn-vue).
- Primo dominio applicativo implementato: modelli `Character`/`CharacterClass`/`CharacterRace` con API di lettura + update vitals (`GET /api/characters/`, `GET /api/characters/{id}`, `PATCH /api/characters/{id}/vitals`, più i corrispondenti endpoint di lettura per classi/razze), e relativa UI (`frontend/src/pages/character.vue` + composable `useCharacter`, vedi sopra). Migrazioni Alembic presenti per tabelle, seed dati di riferimento e aggiunta hit points.
- **Modello di dominio esteso** (vedi `docs/character-domain-model.md` per il razionale su razza/classe come entità): oltre a `CharacterClass`/`CharacterRace`, ora anche `CharacterSubclass` (FK opzionale su `Character`); tabelle di riferimento `Weapon`/`Armor` (seedate via Alembic); competenze modellate come `RaceProficiency`/`ClassProficiency`/`SubclassProficiency` (grant per arma specifica o categoria arma/armatura, con `min_level` per classe/sottoclasse). Pattern **dato derivato vs dato salvato**: `GET /api/characters/{id}/proficiencies` non legge un campo sul personaggio, ma risolve a runtime le competenze da razza + classe + sottoclasse (filtrate per livello) e ne fa il merge (stessa competenza da più fonti → una riga sola, priorità sottoclasse > classe > razza); nessuna competenza è duplicata/salvata sul `Character`.
- **Nuovi domini applicativi:** inventario oggetti (`InventoryItem`, CRUD completo su `/api/characters/{id}/inventory`, UI in `InventoryCard.vue` + `ItemFormDialog.vue` + composable `useInventory`) e valute (campi `*_pieces` su `Character`, update via `PATCH .../currency`, UI in `CurrencyTracker.vue`).
- **Tiri di dado lato UI:** composable `useDiceRoll.ts` (d4/d6/d8/d10/d12/d20/d100, calcolo locale, nessuna chiamata al backend) usato da più card (Abilità, Prove di Salvezza, Tiri Rapidi) per mostrare il risultato via toast (vedi vue-sonner sopra). Logica di regolamento D&D (modificatori, bonus di competenza per livello, percezione passiva) centralizzata in `frontend/src/lib/dnd.ts`, non duplicata per componente.
- **Da allineare:** la pagina attuale è ancora `src/pages/character.vue` (nome singolare, piatta, `character_id` hardcoded, ora a `4`), mentre la convenzione di routing documentata sopra prevede `characters/[id].vue` + sotto-pagine. Il refactor verso quella struttura resta rimandato a quando arriveranno selezione personaggio e sezioni incantesimi — nonostante l'aggiunta di inventario/competenze, non ancora una necessità concreta (vedi trigger Pinia sopra, anch'essi non ancora scattati).
- Le decisioni sopra sono definitive per l'avvio del progetto ma non immutabili: se emergono esigenze concrete (es. tanta gestione di dati di reference), rivalutarle.
- Aggiornare questo documento quando si prendono nuove decisioni architetturali rilevanti (es. autenticazione, hosting/deploy, convenzioni API).
