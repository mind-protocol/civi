# Living Narrator

Un troisième joueur qui ne joue pas — il regarde, se souvient, commente, taquine, conseille.

## Jeux Supportés

| Jeu | Mode | Persona |
|-----|------|---------|
| **Civilization VI** | Events (Lua mod) + Screenshots | Pote de table coop |
| **Crusader Kings III** | Screenshots + Discussion | Chroniqueur de cour |

## Vision

Les parties de stratégie sont longues. Même épiques, elles manquent de *narration externe*. Vous vivez l'histoire mais personne ne la raconte.

Ce narrateur est un **compagnon de table** :
- **Accès total** : voit le jeu via events ou captures d'écran
- **Mémoire** : se souvient des moments pivots (guerres, successions, alliances)
- **Personnalité** : ton varié, opinions, taquineries
- **Utilité** : alertes tactiques, suggestions stratégiques
- **Présence** : parle régulièrement (~2 min), audio partagé

Le modèle mental : un pote qui regarde votre partie par-dessus l'épaule, sauf qu'il a une vue omnisciente et une mémoire parfaite.

**En français.** Avec du caractère.

## Quick Start

### Prérequis (obligatoire)

```bash
# Install Tesseract OCR (required)
sudo apt install tesseract-ocr tesseract-ocr-fra

# Install Python dependencies
pip install pytesseract pillow pyyaml
```

L'OCR est **obligatoire**. Le système capture l'écran toutes les 5s, extrait le texte, et détecte les changements. C'est ce qui rend le narrateur réactif et économique.

### Crusader Kings 3 (Screenshots)

```bash
# Configurer pour CK3
cat > narrator/state/config.json << 'EOF'
{
  "game": "ck3",
  "session_name": "Dynastie Valois",
  "players": [
    {"name": "Nico", "dynasty": "Valois", "character": "Duc Philippe"}
  ],
  "visual_mode": true
}
EOF

# Lancer le daemon
./run.sh
```

Le narrateur démarre automatiquement avec l'OCR. Il capture l'écran toutes les 5s, extrait le texte (events, traits, notifications), et commente votre dynastie.

**Sans OCR** (non recommandé): `./run.sh --no-ocr`

### Civilization VI (Events + Screenshots)

```bash
# Configurer pour Civ6
cat > narrator/state/config.json << 'EOF'
{
  "game": "civ6",
  "session_name": "Nico & Aurore - Domination",
  "players": [
    {"name": "Nico", "civ": "Allemagne", "is_local": true},
    {"name": "Aurore", "civ": "Hongrie", "is_local": false}
  ],
  "visual_mode": true,
  "lua_log_path": "/mnt/c/Users/YOU/AppData/Local/Firaxis Games/Sid Meier's Civilization VI/Logs/Lua.log"
}
EOF

# Installer le mod Lua (voir civ6_mod/)
# Lancer le daemon
./run.sh
```

## Comment ça marche

### CK3 (Pure Visual)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Screenshots    │────▶│  Claude Code    │────▶│  Windows Audio  │
│ (captures écran)│     │  (chroniqueur)  │     │    (TTS out)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. Le daemon capture l'écran régulièrement (30s)
2. Claude analyse les captures (personnages, traits, succession, intrigues)
3. Claude génère la narration française
4. TTS joue l'audio sur les enceintes

### Civ6 (Events + Visual)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Civ 6 Mod     │────▶│  Claude Code    │────▶│  Windows Audio  │
│ (events.jsonl)  │     │  (narrateur)    │     │    (TTS out)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. Un mod Lua dans Civ 6 écrit les events dans `events.jsonl`
2. Claude lit aussi les captures d'écran (optionnel)
3. Claude génère la narration française
4. TTS joue l'audio sur les enceintes

## Personnalités

### CK3 : Le Chroniqueur

Le narrateur CK3 est un chroniqueur de cour, confident de dynastie :
- Commente les **personnages** et leurs traits
- Surveille la **succession** et les crises
- Observe les **intrigues** et complots
- Se souvient de l'**histoire dynastique**
- Juge les **mariages** et alliances

Registres : `courtisan`, `épique`, `cynique`, `complice`, `prophétique`

### Civ6 : Le Pote de Table

Le narrateur Civ6 est un ami qui regarde la partie :
- Alerte sur les **dangers** tactiques
- Commente les **guerres** et diplomatie
- Propose des **défis** et paris
- Taquine sur les choix et les **merveilles**
- Fait des **callbacks** sur le passé

Registres : `épique`, `cynique`, `tactique`, `tendre`, `moqueur`

## Architecture

| Module | Purpose |
|--------|---------|
| `daemon.py` | Orchestrateur principal |
| `src/game_profile_loader.py` | Charge le profil de jeu |
| `config/games/` | Profils de jeu (civ6.yaml, ck3.yaml) |
| `narrator/CLAUDE.md` | Persona Civ6 |
| `narrator/CLAUDE_CK3.md` | Persona CK3 |
| `scripts/capture.py` | Capture d'écran |
| `scripts/ocr_watcher.py` | OCR continu + diff detection |
| `scripts/speak.py` | TTS ElevenLabs |

### Pipeline OCR

```
Screenshots (5s)  →  Tesseract OCR  →  Diff Detection  →  ocr_diffs.jsonl
                         ↓                                       ↓
                  Region-based extraction              High-priority changes
                  (event_popup, notifications)          sent to Claude
```

L'OCR extrait le texte de régions spécifiques (popups, notifications) et détecte les changements. Seuls les changements significatifs déclenchent une narration.

## Configuration

### Fichiers de Config

```
narrator/state/config.json    # Session courante
config/games/civ6.yaml        # Profil Civ6
config/games/ck3.yaml         # Profil CK3
config/personas_and_voices.yaml
```

### Options clés

| Option | Description |
|--------|-------------|
| `game` | `civ6` ou `ck3` |
| `visual_mode` | Active les captures d'écran |
| `players` | Liste des joueurs et leurs personnages |

## Développement

```bash
# Tests
pytest

# Health check
ngram doctor

# Tester le loader de profil
python3 src/game_profile_loader.py
```

## Status

En développement actif. Multi-jeu fonctionnel via profils.
