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

### Modelli e migrazioni: SQLModel + Alembic

- **SQLModel** unifica modello DB e schema API in un'unica classe, riducendo il boilerplate tra layer di persistenza e layer di validazione/serializzazione.
- **Alembic** gestisce le migrazioni su Postgres: autogenerate confrontando i modelli con lo stato del DB, supporto upgrade/downgrade. SQLModel non sostituisce Alembic: le migrazioni si fanno comunque con Alembic.

### Tipi frontend da OpenAPI: openapi-typescript

- FastAPI espone automaticamente lo schema OpenAPI (`/openapi.json`); da questo si generano i tipi TypeScript per Vue con **openapi-typescript**, evitando di duplicare a mano le interfacce dei modelli lato frontend.
- Genera solo i tipi (non un client HTTP completo): il client per le chiamate (fetch/Axios) resta scritto a mano, tipizzato con i tipi generati. Scelta più controllabile rispetto a tool che generano anche il client (es. orval), a costo di un minimo di boilerplate in più sulle chiamate.
- Da rilanciare come script (es. `npm run gen:api`) ogni volta che lo schema del backend cambia; non è una sincronizzazione automatica/live.

### CSS e componenti UI: Tailwind + shadcn-vue/Reka UI

- **Tailwind CSS** per lo styling: utility-first, nessun foglio di stile separato da mantenere in parallelo ai componenti.
- Per i widget (dialog, dropdown, tabs, tooltip, ecc.) si è scelto un approccio **headless** invece di una libreria "tutto incluso" (es. PrimeVue, Vuetify): **Reka UI** fornisce i componenti primitivi (comportamento, accessibilità, gestione focus/tastiera/ARIA) senza alcuno stile imposto; **shadcn-vue** è la libreria di componenti pre-costruiti sopra Reka UI, distribuita come codice da copiare nel progetto (non un package da installare) così che lo stile Tailwind applicato sia interamente personalizzabile.
- Scelta guidata dalla volontà di un design totalmente personalizzabile, senza il "look" riconoscibile delle librerie tutto-incluso e senza rischio di funzionalità premium a pagamento.
- **Compromesso accettato:** per componenti complessi come tabelle con sort/filtri/paginazione non c'è un widget già pronto: va usata una libreria headless dedicata (es. **TanStack Table**) per la logica, con markup e stile scritti a mano. Richiede più lavoro iniziale rispetto a un kit all-in-one.

## Note per contesti futuri

- Il progetto è agli inizi: al momento della stesura di questo documento il repository contiene solo `LICENSE` e questo file, nessun codice.
- Le decisioni sopra sono definitive per l'avvio del progetto ma non immutabili: se emergono esigenze concrete (es. tanta gestione di dati di reference), rivalutarle.
- Aggiornare questo documento quando si prendono nuove decisioni architetturali rilevanti (es. autenticazione, hosting/deploy, struttura cartelle, convenzioni API).
