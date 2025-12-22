# Civ6 Living Narrator

Un troisième joueur qui ne joue pas — il regarde, se souvient, commente, taquine, conseille.

## Vision

Les parties de Civ 6 en coop sont longues (30h+). Même épiques, elles manquent de *narration externe*. Vous vivez l'histoire mais personne ne la raconte.

Ce narrateur est un **compagnon de table** :
- **Accès total** : voit le game state des deux côtés
- **Mémoire** : se souvient des moments pivots
- **Personnalité** : ton varié, opinions, taquineries
- **Utilité** : alertes tactiques, suggestions stratégiques
- **Présence** : parle régulièrement (~2 min), audio partagé

Le modèle mental : un pote qui regarde votre partie par-dessus l'épaule, sauf qu'il a une vue omnisciente et une mémoire parfaite.

**En français.** Avec du caractère.

## Principes

**Présence > Précision.** Le narrateur peut se tromper. Il ne peut pas être absent. Une ligne approximative toutes les 2 min vaut mieux qu'une analyse parfaite toutes les 10 min.

**Variation obligatoire.** Cinq registres en rotation : épique, cynique, tactique, tendre, moqueur. Jamais deux fois le même ton.

**Complicité, pas autorité.** Il suggère ("je dis ça, je dis rien"), il ne juge pas ("mauvaise décision"). C'est un pote, pas un coach.

**Personnalité assumée.** Il peut donner son avis, proposer des challenges, critiquer gentiment, prendre parti, spéculer.

## Comment ça marche

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Civ 6 Mod     │────▶│  Claude Code    │────▶│  Windows Audio  │
│ (events.jsonl)  │     │  (narrateur)    │     │    (TTS out)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. Un mod Lua dans Civ 6 écrit les events dans `events.jsonl`
2. Claude Code (monothread, `--continue`) décide quand parler
3. Claude génère la narration française
4. TTS (Eleven Labs / autre) joue l'audio sur les enceintes

Le narrateur tourne sur WSL. Civ 6 et l'audio tournent sur Windows.

## Quick Start

```bash
# Lance le narrateur (mode continu)
./run.sh

# Une seule itération (process events et exit)
./step.sh
```

## Ce que le narrateur fait

| Type | Exemple |
|------|---------|
| **Alerte** | "Ton archer à Memphis a trois épées sur le dos." |
| **Conseil** | "Gilgamesh a dégarni son nord... je dis ça, je dis rien." |
| **Callback** | "Depuis la chute d'Alexandrie, tu construis différemment." |
| **Pivot** | "L'Histoire retiendra ce moment." |
| **Taquinerie** | "Encore une merveille. Tu compenses quelque chose ?" |
| **Challenge** | "Et si tu prenais cette ville en 10 tours ?" |
| **Ambient** | "Le calme. Ce genre de calme qui précède." |

## Architecture

| Module | Purpose |
|--------|---------|
| `src/ingest/` | Parse les events du jeu |
| `src/llm_router/` | Route vers Claude, JSON strict |
| `src/moment_graph/` | Mémoire des pivots narratifs |
| `runtime_windows/` | Audio playback Windows |
| `agents/narrator/` | Identité et voix du narrateur |

## Configuration

```
config/
├── config.yaml              # Paramètres système
├── personas_and_voices.yaml # Voix et personnalité
└── session_init.yaml        # Map, civs, joueurs (à remplir)
```

## Le Narrateur

Extrait de `agents/narrator/CLAUDE.md` :

> Tu es un compagnon de table pour une partie de Civilization VI.
> Tu vois tout, tu te souviens, tu commentes avec personnalité.
>
> **Toujours en français.** Avec du caractère.

Registres : `épique`, `cynique`, `tactique`, `tendre`, `moqueur`

## Ce que ce n'est PAS

- **Pas un commentateur exhaustif.** Il ne couvre pas chaque event.
- **Pas neutre.** Il a des opinions, il prend parti, il taquine.
- **Pas infaillible.** Il peut se tromper. C'est ok — c'est un pote, pas un oracle.

## Développement

```bash
# Tests
pytest

# Health check
ngram doctor

# Contexte d'un fichier
ngram context <file>
```

Voir `docs/civ6_living_narrator/` pour la doc chain complète.

## Status

En développement actif. Proto fonctionnel, on affine le ton et le rythme.
