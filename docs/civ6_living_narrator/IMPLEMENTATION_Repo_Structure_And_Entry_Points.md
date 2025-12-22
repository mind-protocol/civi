# Living Narrator — Implementation: Code Architecture and Structure

```
STATUS: DRAFT
CREATED: 2024-12-22
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Product_And_Feelings.md
BEHAVIORS:      ./BEHAVIORS_System_Experience_And_Rhythm.md
PATTERNS:       ./PATTERNS_System_Architecture_And_Boundaries.md
MECHANISMS:     ./MECHANISMS_Narrator_Core_Systems.md
ALGORITHM:      ./ALGORITHM_End_To_End_Pipeline.md
VALIDATION:     ./VALIDATION_Global_Invariants_And_Budgets.md
THIS:           ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           narrator/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
living-narrator/
├── daemon.py                     # Orchestrateur (poll + lance Claude)
├── narrator/
│   ├── CLAUDE.md                 # Identity + instructions pour Claude Code
│   └── state/
│       ├── game_state.json       # ← Lua (lu à chaque cycle)
│       ├── events.jsonl          # ← Lua (tail à chaque cycle)
│       ├── config.json           # Setup session (lu une fois)
│       ├── status.json           # État daemon/Claude
│       ├── cursor.json           # Dernier event traité
│       ├── history.json          # Backup narrations (écrit, rarement lu)
│       ├── moments.json          # Backup pivots (écrit, rarement lu)
│       ├── threads.json          # Backup arcs narratifs (écrit, rarement lu)
│       └── ideas.json            # Backup idées (écrit, rarement lu)
├── scripts/
│   ├── speak.py                  # TTS Eleven Labs + playback
│   └── validate_session.py       # Analyse post-session
├── civ6-mod/
│   ├── LivingNarrator.modinfo
│   └── Scripts/
│       └── LivingNarrator.lua    # Export game state + events
└── audio/
    └── (cache TTS)
```

### Architecture Decision: Jamais de Reset

**Claude garde tout le contexte de la session.** Il ne relit pas `history.json`, `moments.json`, etc. à chaque cycle — il sait déjà. Ces fichiers existent pour :
1. Persistance en cas de crash catastrophique
2. Analyse post-session
3. Reconstruction si nécessaire

**Claude lit à chaque cycle :**
- `game_state.json` — état actuel (change constamment)
- `events.jsonl` depuis cursor — nouveaux events

**Claude lit une fois au début :**
- `config.json` — setup de session

### File Responsibilities

| File | Purpose | Key Elements | Status |
|------|---------|--------------|--------|
| `CLAUDE.md` | Identité du narrateur, instructions, exemples de tons | Prompt système | À CRÉER |
| `game_state.json` | État complet du jeu refreshé ~30s | Joueurs, villes, unités, diplo | RUNTIME |
| `events.jsonl` | Stream append-only des events | Un JSON par ligne | RUNTIME |
| `moments.json` | Mémoire des pivots narratifs | Max ~20 moments actifs | RUNTIME |
| `history.json` | Dernières narrations | Pour éviter répétition | RUNTIME |
| `config.json` | Setup de session | Map, civs, noms joueurs | MANUEL AU DÉBUT |
| `LivingNarrator.lua` | Mod Civ 6 qui exporte tout | Listeners + dump | À CRÉER |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Agent Claude Code monothread avec état fichier

**Why this pattern:**
- Pas de serveur à maintenir
- Claude gère lui-même le timing via `--continue`
- État persisté en fichiers simples (JSON)
- Tool use pour lire state, écrire narrations, appeler TTS

### Patterns en Usage

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Append-only log | `events.jsonl` | Jamais de perte d'events, facile à tail |
| Snapshot state | `game_state.json` | État complet à chaque refresh, pas de delta |
| Rolling window | `history.json` | Garde seulement les N dernières narrations |
| Bounded memory | `moments.json` | Max 20 moments, garbage collection |

### Anti-Patterns à Éviter

- **Polling agressif** : Claude ne doit pas lire le state en boucle serrée → cooldown entre lectures
- **State en mémoire Claude** : Tout doit être persisté en fichiers, Claude peut restart
- **Events processing exhaustif** : Pas besoin de traiter chaque event, on résume

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Civ 6 → Narrator | Game state, events | Logique narrative | Fichiers JSON |
| Narrator → TTS | Texte français | Audio bytes | API call |
| Claude → État | Décisions narratives | Persistence | Tool read/write |

---

## SCHEMA

### GameState

```yaml
GameState:
  required:
    - ts: string              # ISO timestamp du dump
    - turn: int               # Tour actuel
    - players: Player[]       # Tous les joueurs
  optional:
    - cities: dict            # player_id → City[]
    - military: dict          # player_id → MilitaryCounts
    - diplomacy: dict         # player_id → {other_id: relation}
```

### Player

```yaml
Player:
  required:
    - id: int
    - civ: string             # "CIVILIZATION_ROME"
    - leader: string          # "LEADER_TRAJAN"
    - is_human: bool
    - is_alive: bool
  optional:
    - era: int
    - gold: int
    - military_strength: int
    - science_per_turn: int
    - culture_per_turn: int
```

### City

```yaml
City:
  required:
    - name: string
    - population: int
    - x: int
    - y: int
    - is_capital: bool
  optional:
    - is_under_siege: bool
    - production: string      # Ce qui est en construction
    - walls: bool
```

### Event

```yaml
Event:
  required:
    - ts: string              # ISO timestamp
    - turn: int
    - type: string            # WAR_DECLARED, CITY_CAPTURED, etc.
  optional:
    - actor: {id, civ, leader}
    - target: {id, civ, leader}
    - payload: object         # Détails spécifiques au type
```

### Moment

```yaml
Moment:
  required:
    - id: string              # UUID
    - turn_created: int
    - type: string            # war, city_fall, wonder, betrayal
    - description: string     # "Rome déclare la guerre à l'Égypte"
    - actors: int[]           # player_ids impliqués
  optional:
    - emotional_charge: high | medium | low
    - callback_count: int     # Fois référencé
    - last_callback_turn: int
```

### Narration

```yaml
Narration:
  required:
    - ts: string
    - turn: int
    - text: string            # Le texte dit
    - tone: string            # epic, cynical, tactical, tender, mocking
    - type: string            # pivot, alert, advice, callback, summary, tease, ambient, challenge
  optional:
    - moment_refs: string[]   # IDs des moments référencés
    - players_mentioned: int[] # Pour tracking équilibre
```

### SessionConfig

```yaml
SessionConfig:
  required:
    - map_type: string        # "TSL Europe"
    - human_players:
        - name: string        # "Nicolas"
          civ: string         # "Rome"
          player_id: int
        - name: string        # "Aurore"
          civ: string         # "Egypt"
          player_id: int
    - victory_type: string    # "domination"
  optional:
    - game_speed: string
    - difficulty: string
    - notes: string           # Contexte additionnel
```

---

## ENTRY POINTS

| Entry Point | Triggered By | Description |
|-------------|--------------|-------------|
| Claude Code `--continue` | Timer/Manuel | Reprend le loop narrateur |
| Lecture `game_state.json` | Tool call | Récupère état actuel |
| Lecture `events.jsonl` | Tool call | Récupère nouveaux events |
| Écriture `moments.json` | Tool call | Persiste nouveau moment |
| Écriture `history.json` | Tool call | Persiste narration |
| Appel TTS API | Tool call | Génère et joue audio |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Flow 1: Game State Ingestion

Ce flow récupère l'état du jeu depuis le fichier exporté par le mod Lua.

```yaml
flow:
  name: state_ingestion
  purpose: Alimenter Claude avec l'état actuel du jeu
  scope: Fichier → Contexte Claude
  steps:
    - id: lua_dump
      description: Le mod Lua écrit le game state
      file: civ6-mod/Scripts/LivingNarrator.lua
      output: narrator/state/game_state.json
      trigger: Toutes les 30 secondes ou fin de tour
      side_effects: Écrase le fichier précédent

    - id: claude_read
      description: Claude lit le state via tool
      input: narrator/state/game_state.json
      output: Contexte en mémoire Claude
      trigger: Début de cycle narrateur

  docking_points:
    available:
      - id: state_file_written
        type: file
        direction: output
        file: narrator/state/game_state.json
        trigger: Lua dump complete
        payload: GameState

      - id: state_file_read
        type: file
        direction: input
        file: narrator/state/game_state.json
        trigger: Claude tool call
        payload: GameState

    health_recommended:
      - dock_id: state_file_written
        reason: Vérifier fraîcheur (timestamp < 60s)
```

### Flow 2: Event Ingestion

Ce flow récupère les events récents depuis le stream append-only.

```yaml
flow:
  name: event_ingestion
  purpose: Capturer les events du jeu pour réaction narrative
  scope: Fichier → Buffer Claude
  steps:
    - id: lua_append
      description: Le mod Lua append chaque event
      file: civ6-mod/Scripts/LivingNarrator.lua
      output: narrator/state/events.jsonl
      trigger: Chaque event in-game
      side_effects: Append au fichier

    - id: claude_tail
      description: Claude lit les nouvelles lignes
      input: narrator/state/events.jsonl
      output: Liste d'events en mémoire
      trigger: Début de cycle narrateur

    - id: claude_mark_processed
      description: Claude note où il en est
      side_effects: Stocke last_processed_line ou timestamp

  docking_points:
    available:
      - id: event_appended
        type: file
        direction: output
        file: narrator/state/events.jsonl
        payload: Event (une ligne JSON)

      - id: events_read
        type: file
        direction: input
        file: narrator/state/events.jsonl
        payload: Event[]

    health_recommended:
      - dock_id: event_appended
        reason: Vérifier que les events arrivent
```

### Flow 3: Narration Generation

Ce flow produit le texte narratif basé sur le contexte.

```yaml
flow:
  name: narration_generation
  purpose: Produire le commentaire du narrateur
  scope: État + Events + History → Texte français
  steps:
    - id: context_assembly
      description: Claude assemble le context pack
      input: game_state, events, moments, history, config
      output: Contexte structuré pour génération

    - id: decision
      description: Claude décide type + ton
      input: Contexte assemblé
      output: {content_type, tone}

    - id: generation
      description: Claude génère le texte
      input: Contexte + décisions
      output: Texte narratif français

    - id: validation
      description: Claude vérifie cohérence
      input: Texte généré
      output: Texte validé ou régénération

  docking_points:
    available:
      - id: narration_generated
        type: event
        direction: output
        payload: Narration
        notes: Moment où le texte est prêt

    health_recommended:
      - dock_id: narration_generated
        reason: Vérifier timing et variation de ton
```

### Flow 4: Audio Output

Ce flow transforme le texte en audio joué.

```yaml
flow:
  name: audio_output
  purpose: Parler le texte via TTS
  scope: Texte → Audio enceintes
  steps:
    - id: tts_call
      description: Appel API TTS (Eleven Labs ou autre)
      input: Texte français
      output: Audio bytes ou URL
      trigger: Narration prête

    - id: playback
      description: Jouer l'audio sur les enceintes
      input: Audio
      output: Son audible
      side_effects: Aurore et Nicolas entendent

  docking_points:
    available:
      - id: tts_request
        type: api
        direction: output
        payload: {text, voice, language}

      - id: tts_response
        type: api
        direction: input
        payload: audio_bytes ou audio_url

      - id: audio_played
        type: event
        direction: output
        notes: Confirmation playback terminé

    health_recommended:
      - dock_id: audio_played
        reason: Vérifier que l'audio joue effectivement
```

### Flow 5: Memory Persistence

Ce flow gère la mémoire narrative (moments + history).

```yaml
flow:
  name: memory_persistence
  purpose: Maintenir la continuité narrative entre cycles
  scope: Décisions Claude → Fichiers JSON
  steps:
    - id: moment_creation
      description: Si pivot détecté, créer un moment
      input: Event majeur
      output: Nouveau Moment
      trigger: Event type in [WAR_DECLARED, CITY_CAPTURED, ...]

    - id: moment_write
      description: Persister le moment
      output: narrator/state/moments.json
      side_effects: Ajout au fichier, possible GC

    - id: history_write
      description: Persister la narration
      output: narrator/state/history.json
      side_effects: Ajout, rolling window (garder N dernières)

  docking_points:
    available:
      - id: moments_updated
        type: file
        direction: output
        file: narrator/state/moments.json
        payload: Moment[]

      - id: history_updated
        type: file
        direction: output
        file: narrator/state/history.json
        payload: Narration[]

    health_recommended:
      - dock_id: moments_updated
        reason: Vérifier bounded memory (max 20)
```

---

## LOGIC CHAINS

### LC1: Cycle Complet Narrateur

**Purpose:** Un cycle complet de "lire → décider → parler → persister"

```
[Claude wakes up via --continue]
  ↓
read(game_state.json)         # État actuel
  ↓
read(events.jsonl)            # Nouveaux events
  ↓
read(moments.json)            # Mémoire narrative
  ↓
read(history.json)            # Narrations récentes
  ↓
decide(should_speak?)         # Timing ok ?
  ↓
IF yes:
  select(content_type, tone)  # Quoi dire, comment
    ↓
  generate(narration)         # Texte français
    ↓
  call(TTS)                   # Audio
    ↓
  play(audio)                 # Enceintes
    ↓
  persist(history, moments)   # Mise à jour mémoire
  ↓
sleep(30-60s)                 # Attendre avant prochain cycle
  ↓
[--continue]
```

### LC2: Création de Moment

**Purpose:** Transformer un event majeur en moment narratif

```
event(WAR_DECLARED, Rome → Egypt)
  ↓
evaluate(is_pivot?)           # Oui, guerre implique humains
  ↓
create_moment({
  type: "war",
  description: "Rome déclare la guerre à l'Égypte",
  actors: [rome_id, egypt_id],
  emotional_charge: "high"
})
  ↓
append(moments.json)
  ↓
IF moments.length > 20:
  garbage_collect()           # Virer les plus vieux/moins chargés
```

### LC3: Callback Check

**Purpose:** Trouver un moment qui résonne avec le présent

```
current_situation(war with Sumeria)
  ↓
scan(moments)
  ↓
FOR each moment:
  IF moment.actors overlaps current_actors:
    IF moment.last_callback_turn < turn - 20:
      candidate = moment
  ↓
IF candidate:
  return {type: "callback", moment: candidate}
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
CLAUDE.md (identity)
    └── uses → state/*.json (data)
    └── calls → TTS API (audio)
```

### External Dependencies

| Package/Service | Used For | Called By |
|-----------------|----------|-----------|
| Eleven Labs API | TTS voix française | `scripts/speak.py` via bash |
| Claude Code | Narrateur (monothread, --continue) | `daemon.py` |
| Civ 6 + Mod Lua | Source des données | Externe |

### Daemon Orchestration

```
daemon.py (Python, tourne en fond)
    ↓
poll status.json + events.jsonl
    ↓
if should_narrate:
    status.json ← claude_running = true
    subprocess: claude --continue -p narrator
    status.json ← claude_running = false
```

**Timing:**
- CHECK_INTERVAL: 10s (fréquence poll)
- MIN_NARRATION_INTERVAL: 30s
- TARGET_NARRATION_INTERVAL: 120s (~2 min)
- URGENT_EVENTS bypass le timer

### Windows ↔ WSL Bridge

Le mod Lua (Civ 6, Windows) écrit dans un dossier Windows :
```
C:\Users\<you>\Documents\Civ6Narrator\
├── game_state.json
└── events.jsonl
```

WSL lit ce dossier via mount :
```
/mnt/c/Users/<you>/Documents/Civ6Narrator/
```

Config dans `narrator/state/config.json` :
```json
{
  "windows_state_path": "/mnt/c/Users/Nicolas/Documents/Civ6Narrator/"
}
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Game state | `state/game_state.json` | Session | Refresh ~30s par Lua |
| Events | `state/events.jsonl` | Session | Append-only par Lua |
| Moments | `state/moments.json` | Session | Géré par Claude, max 20 |
| History | `state/history.json` | Session | Rolling window, N dernières |
| Config | `state/config.json` | Session | Manuel au début |

### State Transitions

```
[Session Start]
    ↓
config.json créé (manuel)
    ↓
[Game Running]
    ↓
game_state.json ←── Lua refresh
events.jsonl ←── Lua append
moments.json ←→ Claude read/write
history.json ←→ Claude read/write
    ↓
[Session End]
    ↓
Fichiers conservés pour analyse post-session
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Créer/vérifier config.json avec setup de session
2. Vider ou archiver events.jsonl de session précédente
3. Lancer le mod Lua dans Civ 6
4. Lancer Claude Code avec CLAUDE.md
5. Premier cycle : lecture état, premier commentaire "La partie commence..."
```

### Main Loop

```
1. Claude wake up (--continue)
2. Lire tous les fichiers state
3. Évaluer si c'est le moment de parler (timing + events)
4. Si oui : générer, TTS, play, persister
5. Si non : log "skipped", noter dernier check
6. Sleep implicite (Claude attend --continue)
```

### Shutdown

```
1. Dernier commentaire possible ("La session se termine...")
2. Sauvegarder state final
3. Logs de session conservés pour analyse
```

---

## CONCURRENCY MODEL

**Mono-thread.** Claude Code tourne seul. Le mod Lua tourne dans Civ 6. Pas de concurrence à gérer côté narrateur.

Seul point d'attention : le mod Lua écrit pendant que Claude lit. Solution : Claude lit le fichier entier (snapshot), pas de streaming partiel.

---

## CONFIGURATION

### config.json (exemple)

```json
{
  "map_type": "TSL Europe",
  "human_players": [
    {"name": "Nicolas", "civ": "Rome", "player_id": 0},
    {"name": "Aurore", "civ": "Egypt", "player_id": 1}
  ],
  "victory_type": "domination",
  "game_speed": "standard",
  "difficulty": "deity",
  "tts": {
    "service": "elevenlabs",
    "voice_id": "xxx",
    "language": "fr"
  },
  "timing": {
    "target_interval_seconds": 120,
    "min_interval_seconds": 30,
    "max_interval_seconds": 180
  }
}
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Reference |
|------|-----------|
| `CLAUDE.md` | Réfère à PATTERNS, BEHAVIORS |
| `LivingNarrator.lua` | Réfère au SCHEMA pour format export |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| M1 Timing | `CLAUDE.md` instructions |
| M2 Classification | `CLAUDE.md` instructions |
| M3 Rotation Ton | `CLAUDE.md` instructions |
| M4 Mémoire Pivots | `moments.json` + `CLAUDE.md` |
| M5 Analyse Tactique | `CLAUDE.md` instructions |
| M8 TTS | Tool call dans `CLAUDE.md` |

---

## FICHIERS À CRÉER

| Fichier | Priorité | Description |
|---------|----------|-------------|
| `CLAUDE.md` | P0 | Identité + instructions complètes |
| `LivingNarrator.lua` | P0 | Mod Civ 6 export |
| `config.json` template | P1 | Template de config session |
| `validate_session.py` | P2 | Analyse post-session |

---

## MARKERS

<!-- @ngram:todo Créer CLAUDE.md avec identité narrateur -->
<!-- @ngram:todo Finaliser le mod Lua -->
<!-- @ngram:todo Choisir et configurer service TTS -->
<!-- @ngram:proposition Ajouter un dashboard live des métriques si utile -->
