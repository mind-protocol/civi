# Installation du Mod Living Narrator

## Fichiers du Mod

```
civ6_mod/
├── LivingNarrator.modinfo
└── Scripts/
    ├── JSONSerializer.lua
    ├── FileWriter.lua
    └── LivingNarrator.lua
```

## Installation

### 1. Trouver le dossier Mods de Civ 6

**Windows:**
```
C:\Users\<TON_NOM>\Documents\My Games\Sid Meier's Civilization VI\Mods\
```

### 2. Copier le mod

Copier le dossier `civ6_mod` dans le dossier Mods et le renommer `LivingNarrator`:

```
Mods/
└── LivingNarrator/
    ├── LivingNarrator.modinfo
    └── Scripts/
        ├── JSONSerializer.lua
        ├── FileWriter.lua
        └── LivingNarrator.lua
```

### 3. Activer le mod

1. Lancer Civilization VI
2. Menu principal → **Additional Content**
3. Activer **Living Narrator - Event Exporter**
4. Lancer une partie

## Fichiers Produits

Le mod crée automatiquement:

```
C:\Users\Nicolas\Documents\Civ6Narrator\
├── events.jsonl      # Stream d'événements (append)
└── game_state.json   # État complet (mis à jour à chaque tour)
```

## Commandes Console (Debug)

Dans la console Lua de Civ 6 (Firetuner ou tilde):

- `LN_Status()` — Afficher l'état du mod
- `LN_TestEvent()` — Émettre un événement test
- `LN_DumpState()` — Forcer l'export de l'état

## Vérification

Si le mod fonctionne, tu verras dans la console au démarrage:

```
========================================
[LivingNarrator] Initializing v1.0.0
========================================
[LivingNarrator] Game ID: game_1703266800_1234
[LivingNarrator] Local Player: 0
[LivingNarrator] Event file initialized: C:\Users\Nicolas\Documents\Civ6Narrator\events.jsonl
[LivingNarrator] Game state path: C:\Users\Nicolas\Documents\Civ6Narrator\game_state.json
[LivingNarrator] Registering event handlers...
[LivingNarrator] Event handlers registered
[LivingNarrator] Ready!
```

## Problèmes Courants

**"Events not being written"**
- Vérifie que le dossier `Documents\Civ6Narrator` existe ou peut être créé
- Le mod crée le dossier automatiquement, mais les permissions peuvent bloquer

**"Mod not showing in Additional Content"**
- Vérifie que le fichier `.modinfo` est bien à la racine du dossier du mod
- Redémarre Civ 6

**"JSON parse errors"**
- Le fichier events.jsonl s'est peut-être corrompu
- Supprime-le et recommence une partie
