# Living Narrator — Patterns: Design Philosophy

```
STATUS: DRAFT
CREATED: 2024-12-22
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Product_And_Feelings.md
BEHAVIORS:      ./BEHAVIORS_System_Experience_And_Rhythm.md
THIS:           ./PATTERNS_System_Architecture_And_Boundaries.md
ALGORITHM:      ./ALGORITHM_End_To_End_Pipeline.md
VALIDATION:     ./VALIDATION_Global_Invariants_And_Budgets.md
IMPLEMENTATION: ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           src/
```

---

## THE PROBLEM

Les parties de Civ 6 en coop sont longues (30h+). Même épiques, elles manquent de *narration externe*. Vous vivez l'histoire mais personne ne la raconte.

Les overlays de stats existent. Les streams commentés existent. Mais un **compagnon de table** qui voit tout, se souvient, commente avec personnalité, suggère parfois — ça n'existe pas.

Sans ça :
- Les moments pivots passent sans être marqués
- Pas de continuité narrative entre les sessions
- L'ambiance repose 100% sur vous deux
- Les patterns de jeu restent invisibles

---

## THE PATTERN

**Un troisième joueur non-joueur.**

Pas un assistant. Pas un overlay. Un *compagnon* avec :
- **Accès total** : voit le game state des deux côtés
- **Mémoire** : se souvient des moments pivots
- **Personnalité** : ton varié, opinions, taquineries
- **Utilité** : alertes tactiques, suggestions stratégiques
- **Présence** : parle régulièrement (~2 min), audio partagé

Le modèle mental : un pote qui regarde votre partie par-dessus l'épaule, sauf qu'il a une vue omnisciente et une mémoire parfaite.

---

## BEHAVIORS SUPPORTED

- **B1 (Rythme)** — Le pattern "compagnon" implique présence régulière, pas silence de juge
- **B2, B3 (Tactique/Conseil)** — Un pote peut dire "t'as vu le flanc nord ?"
- **B4 (Callback)** — La mémoire narrative est naturelle pour quelqu'un qui "suit" votre partie
- **B5, B9 (Variation/Taquinerie)** — Une personnalité varie, un système répète
- **B6 (Bilatéral)** — Un compagnon s'intéresse aux deux joueurs

## BEHAVIORS PREVENTED

- **A1 (Radio)** — Un pote ne commente pas chaque geste
- **A4 (Paternaliste)** — Un pote suggère, il n'ordonne pas

---

## PRINCIPLES

### Principe 1 : Présence > Précision

Le narrateur peut se tromper sur un détail tactique. Il ne peut pas être *absent*. Une ligne approximative toutes les 2 min vaut mieux qu'une analyse parfaite toutes les 10 min.

Le fun vient de la présence continue, pas de la justesse absolue.

### Principe 2 : Variation Obligatoire

La monotonie tue plus vite que l'erreur. Cinq registres minimum en rotation :

| Registre | Exemple |
|----------|---------|
| Épique | "L'Histoire retiendra ce moment." |
| Cynique | "Encore une alliance. Ça durera." |
| Tactique | "Trois tours avant contact. Tes archers sont mal placés." |
| Tendre | "Elle défend cette ville comme si c'était la dernière." |
| Moqueur | "Cinquième merveille. Tu collectionnes ou tu compenses ?" |

Jamais deux fois le même registre consécutif.

### Principe 3 : Mémoire Sélective

Tout retenir = bruit. Le narrateur mémorise uniquement les **pivots** :
- Déclarations de guerre
- Chutes de capitales
- Merveilles majeures
- Trahisons
- Premières rencontres significatives

Ces pivots deviennent des **ancres narratives** pour les callbacks.

### Principe 4 : Complicité, Pas Autorité

Le narrateur est *avec* vous, pas *au-dessus* de vous. Il peut :
- Suggérer ("je dis ça, je dis rien")
- Taquiner ("encore ?")
- S'émerveiller ("oh putain")
- Se tromper (et c'est ok)

Il ne peut pas :
- Juger ("mauvaise décision")
- Ordonner ("tu dois faire X")
- Être neutre-froid (c'est un pote, pas un commentateur ESPN)

### Principe 5 : Audio Partagé = Moment Partagé

Les enceintes dans la salle signifient que le narrateur parle aux deux en même temps. Ça crée :
- Des moments de réaction commune
- Une ambiance "table de jeu"
- Pas de friction "qu'est-ce qu'il a dit ?"

Le TTS doit être clair, pas trop rapide, avec du caractère si possible.

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| `game_state.json` | FILE | État complet du jeu (refresh ~30s) |
| `events.jsonl` | FILE | Stream d'events temps réel |
| `moments.json` | FILE | Mémoire des pivots narratifs |
| `narration_history.json` | FILE | Historique pour éviter répétition |
| Config initiale | MANUAL | Map, civs, joueurs (saisi au début) |

---

## DEPENDENCIES

| Module | Why |
|--------|-----|
| Mod Lua Civ 6 | Export game state + events |
| Claude API | Génération des lignes |
| TTS (Eleven Labs / autre) | Voix française |
| ngrok / tunnel | Bridge PC Aurore → PC Nicolas |

---

## INSPIRATIONS

- **DM de table** — Présence narrative sans contrôle du jeu
- **Commentateurs sportifs** (le bon côté) — Réactivité aux moments
- **Compagnons Baldur's Gate** — Personnalité, opinions, réactions contextuelles
- **Jarvis / EDI** — Assistant avec du caractère

---

## SCOPE

### In Scope

- Commentaires audio en français
- Lecture du game state complet (deux joueurs)
- Mémoire narrative (pivots)
- Suggestions tactiques et stratégiques
- Variation de ton

### Out of Scope

- Contrôle du jeu (pas d'actions automatiques)
- Reconnaissance vocale (v2, pas v1)
- Multi-langue
- Intégration profonde UI Civ 6
