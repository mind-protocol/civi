# Living Narrator - Test Guide

## Installation du mod

### 1. Copier le mod dans Civ 6

```
Source: civi/civ6_mod/
Destination: %USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI\Mods\LivingNarrator\
```

La structure finale doit être :
```
Documents/My Games/Sid Meier's Civilization VI/Mods/LivingNarrator/
├── LivingNarrator.modinfo
└── Scripts/
    ├── JSONSerializer.lua
    ├── FileWriter.lua
    └── LivingNarrator.lua
```

### 2. Vérifier le dossier de sortie

Le mod écrit dans :
```
%USERPROFILE%\Documents\Civ6Narrator\
```

Ce dossier sera créé automatiquement au premier lancement.

---

## Test en jeu

### Étape 1: Lancer Civ 6 avec le mod

1. Lancer Civ 6
2. Aller dans **Additional Content**
3. Activer **Living Narrator - Event Exporter**
4. Créer une partie (single player suffit pour tester)

### Étape 2: Vérifier les logs

Ouvrir la console Lua ou vérifier `Lua.log` dans :
```
%USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI\Logs\Lua.log
```

Tu devrais voir :
```
========================================
[LivingNarrator] Initializing v1.0.0
========================================
[LivingNarrator] Game ID: game_XXXXX_XXXX
[LivingNarrator] Local Player: 0
[LivingNarrator] Event file initialized: C:\Users\...\Documents\Civ6Narrator\events.jsonl
[LivingNarrator] Game state path: C:\Users\...\Documents\Civ6Narrator\game_state.json
[LivingNarrator] Event handlers registered
[LivingNarrator] Ready!
```

### Étape 3: Vérifier les fichiers de sortie

Après un tour de jeu, vérifier :

```powershell
# Dans PowerShell
Get-Content "$env:USERPROFILE\Documents\Civ6Narrator\events.jsonl" -Tail 10
Get-Content "$env:USERPROFILE\Documents\Civ6Narrator\game_state.json" | ConvertFrom-Json
```

---

## Checklist de test

### Fichiers créés
- [ ] `events.jsonl` existe
- [ ] `game_state.json` existe

### Events capturés
- [ ] `_NARRATOR_STARTUP` dans events.jsonl
- [ ] `GAME_START` dans events.jsonl
- [ ] `TURN_START` après un tour
- [ ] `TURN_END` après fin de tour

### Game state
- [ ] Contient `players` array
- [ ] Chaque player a `cities` et `units`
- [ ] Les positions x/y sont présentes
- [ ] HP des unités visibles

### Events spécifiques (à tester en jouant)
- [ ] `CITY_BUILT` - Fonde une ville
- [ ] `TECH_COMPLETED` - Recherche une tech
- [ ] `CIVIC_COMPLETED` - Complète un civique
- [ ] `WONDER_COMPLETED` - Construit une merveille
- [ ] `WAR_DECLARED` - Déclare une guerre
- [ ] `UNIT_KILLED` - Tue une unité ennemie

---

## Commandes console (debug)

Si la console Lua est accessible (`~` ou via FireTuner) :

```lua
-- Status du mod
LN_Status()

-- Émettre un event test
LN_TestEvent()

-- Forcer l'écriture du game state
LN_DumpState()

-- Tester le serializer JSON
TestJSONSerializer()
```

---

## Problèmes courants

### Le mod ne charge pas
- Vérifier que le dossier est bien dans `Mods/LivingNarrator/`
- Vérifier que `LivingNarrator.modinfo` est à la racine
- Redémarrer Civ 6 après copie

### Pas de fichiers créés
- Vérifier les logs Lua pour les erreurs
- Vérifier les permissions d'écriture dans Documents
- Essayer de créer manuellement `Documents\Civ6Narrator\`

### Events manquants
- Certains events dépendent de la version de Civ 6
- Vérifier dans Lua.log les erreurs de registration

### Multiplayer / Coop
- Le mod fonctionne sur chaque machine séparément
- Le host devrait voir les données de tous les joueurs
- À tester : est-ce que `Players[auroreID]:GetUnits()` retourne les unités du joueur 2 ?

---

## Structure des données

### events.jsonl (exemple)
```json
{"event_type":"_NARRATOR_STARTUP","timestamp":1703261234,"version":"1.0.0"}
{"event_type":"GAME_START","turn":0,"timestamp":1703261235,"game_id":"game_1703261234_5678","local_player_id":0,"local_player_civ":"France","local_player_leader":"Catherine de Medici"}
{"event_type":"TURN_START","turn":1,"timestamp":1703261300,"player_id":0,"player_civ":"France"}
```

### game_state.json (exemple)
```json
{
  "turn": 5,
  "timestamp": 1703261500,
  "game_id": "game_1703261234_5678",
  "players": [
    {
      "id": 0,
      "civ": "France",
      "leader": "Catherine de Medici",
      "is_human": true,
      "gold": 150,
      "techs_researched": 2,
      "civics_researched": 1,
      "cities": [
        {"id": 0, "name": "Paris", "x": 45, "y": 32, "population": 2, "is_capital": true}
      ],
      "units": [
        {"id": 0, "type": "Warrior", "x": 44, "y": 33, "hp": 100, "max_hp": 100}
      ]
    }
  ]
}
```

---

## Prochaines étapes après validation

1. **Si le mod fonctionne** → Tester en coop avec Aurore
2. **Vérifier la visibilité coop** → Est-ce que le host voit les unités du joueur 2 ?
3. **Brancher le daemon** → `daemon.py` lit les fichiers et lance Claude
4. **Tester TTS** → `speak.py` avec Eleven Labs
