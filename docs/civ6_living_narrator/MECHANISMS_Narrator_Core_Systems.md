# Living Narrator — Mécanismes Détaillés

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
THIS:           ./MECHANISMS_Narrator_Core_Systems.md
ALGORITHM:      ./ALGORITHM_End_To_End_Pipeline.md
VALIDATION:     ./VALIDATION_Global_Invariants_And_Budgets.md
IMPLEMENTATION: ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           src/
```

---

## OVERVIEW

Claude Code monothread avec `--continue`. Pas de loop externe — c'est Claude qui décide quand agir.

Huit mécanismes couvrent le cycle complet : timing, classification, ton, mémoire, tactique, équilibrage, contexte, et audio.

---

## M1: Timing Adaptatif

### But
Déterminer le bon moment pour parler. Ni trop souvent (spam), ni trop rare (absence).

### Inputs
- Timestamp du dernier commentaire
- Events reçus depuis le dernier commentaire
- État d'activité du jeu (beaucoup de choses se passent vs calme plat)

### Logique de Décision

**Déclencheur immédiat** : Certains events sont trop importants pour attendre. Guerre déclarée, capitale qui tombe, élimination d'un joueur. Ces events bypassent le timer — on parle maintenant.

**Rythme de base** : En l'absence d'urgence, la cible est ~2 minutes entre commentaires. C'est assez fréquent pour maintenir la présence, assez espacé pour ne pas fatiguer.

**Modulation par activité** : Si beaucoup d'events arrivent (guerre active, expansion rapide), on peut réduire à ~90 secondes. Si c'est le calme plat (développement tranquille, pas de contact), on peut étendre à ~3 minutes.

**Fenêtre d'opportunité** : Entre 90s et 120s, si quelque chose d'intéressant apparaît (callback possible, insight tactique), on parle. Sinon on attend les 120s.

### Edge Cases
- **Deux events urgents en 30 secondes** : On parle sur le premier, on intègre le second dans le prochain commentaire (pas de spam).
- **Joueurs AFK** : Si aucun event depuis 5+ minutes, un commentaire ambient très occasionnel, puis silence.
- **Délibération vocale** : Claude ne peut pas vraiment détecter ça sans micro. On assume que peu d'events = possible délibération, donc on respecte le silence.

---

## M2: Classification de Contenu

### But
Choisir le *type* de commentaire le plus approprié au contexte.

### Types Disponibles

| Type | Description | Exemple |
|------|-------------|---------|
| **Pivot** | L'histoire bascule. Events majeurs — guerre, chute de ville, merveille, paix. | "L'empire s'étend." |
| **Alerte** | Danger immédiat. Unité encerclée, ville menacée, armée qui approche. | "Ton archer a trois épées sur le dos." |
| **Conseil** | Opportunité détectée. Flanc ouvert, ressource libre, timing favorable. | "Je dis ça, je dis rien..." |
| **Callback** | Référence au passé. Moment stocké qui résonne avec le présent. | "Depuis la chute de Carthage..." |
| **Résumé** | Digest de séquence. Events mineurs accumulés sans rien de majeur. | "Beaucoup de bruit. Rien de décisif." |
| **Taquinerie** | Pattern joueur détecté. Comportement répétitif ou prévisible. | "Encore une merveille. Tu compenses ?" |
| **Ambient** | Rien de spécial, mais c'est l'heure. Atmosphère, tension latente. | "Le calme. Ce genre de calme..." |

### Logique de Sélection

```
SI event urgent:
    → Pivot ou Alerte selon le type
SINON:
    Évaluer candidats disponibles:
    - Moment qui résonne ? → Callback possible
    - Danger/opportunité ? → Alerte/Conseil possible
    - Events à condenser ? → Résumé possible
    - Pattern de comportement ? → Taquinerie possible
    - Rien de tout ça ? → Ambient

Pondérer selon:
    - Ce qui a été fait récemment (éviter répétition de type)
    - Pertinence au contexte actuel
```

---

## M3: Rotation de Ton

### But
Éviter la monotonie. Un narrateur qui sonne toujours pareil devient du bruit de fond.

### Registres Disponibles

| Registre | Caractère | Exemple |
|----------|-----------|---------|
| **Épique** | Gravité, grandeur, Histoire | "L'empire s'étend. Le monde n'a pas encore compris." |
| **Cynique** | Recul désabusé, ironie froide | "Une alliance de plus. Ça durera peut-être trois ères." |
| **Tactique** | Précision, urgence contenue | "Deux unités sur ton flanc. Trois tours avant contact." |
| **Tendre** | Émotion, attachement | "Elle défend cette ville comme si tout en dépendait." |
| **Moqueur** | Taquinerie légère, complicité | "Encore une merveille. Tu collectionnes ou tu compenses ?" |

### Règle Cardinale
**Jamais deux tons identiques consécutifs.**

### Affinités Type-Ton

| Type | Tons naturels | Tons évités |
|------|---------------|-------------|
| Pivot | épique, tendre | moqueur |
| Alerte | tactique | - |
| Conseil | tactique, cynique | - |
| Callback | épique, cynique, tendre | - |
| Résumé | cynique, tactique | - |
| Taquinerie | moqueur | - |
| Ambient | tout sauf tactique | tactique |

### Mémoire de Tons
On garde trace des 3-5 derniers tons utilisés pour :
- Éviter la répétition immédiate
- Éviter les patterns (épique-cynique-épique-cynique...)
- Favoriser les tons sous-utilisés récemment

---

## M4: Mémoire de Pivots

### But
Stocker les moments narrativement importants pour callbacks futurs. C'est ce qui crée la continuité sur 30h de jeu.

### Quoi Stocker

| Catégorie | Exemples | Charge |
|-----------|----------|--------|
| Guerres | Qui déclare, contre qui, tour | Haute si joueurs humains |
| Chutes de villes | Quelle ville, qui perd/prend | Capitale > secondaire |
| Merveilles | Les iconiques ou sous pression | Moyenne |
| Trahisons | Alliances brisées, attaques surprises | Haute |
| Premières rencontres | Contact avec civ qui deviendra important | Variable |
| Moments nommés | Ce que les joueurs nomment explicitement | Haute |

### Structure d'un Moment

```yaml
moment:
  description: "Rome déclare la guerre à l'Égypte"
  acteurs: [Rome, Égypte]
  tour: 145
  charge_emotionnelle: haute  # haute/moyenne/basse
  fois_reference: 0
  dernier_callback: null
```

### Quand Faire un Callback

**Résonance thématique** : La situation actuelle fait écho au moment.
- Exemple : moment "Rome déclare la guerre" + event actuel implique Rome

**Cooldown** : Minimum 20-30 tours entre callbacks sur le même moment.

**Charge émotionnelle** : Les moments à haute charge sont callback plus souvent, mais leur charge diminue avec l'usage.

### Gestion de la Mémoire

Maximum ~20 moments actifs. Quand limite approche :
- Moments à basse charge jamais référencés → oubliés
- Moments très anciens sans callback récent → archivés
- Moments à haute charge et callbacks fréquents → persistent

---

## M5: Analyse Tactique

### But
Lire le game state pour détecter dangers et opportunités que les joueurs pourraient manquer.

### Détection de Dangers

**Unité en péril** :
- HP bas (< 50%) ET ennemis à proximité immédiate
- Unité isolée loin de tout soutien
- Unité précieuse (Grand Général, unité unique) exposée

**Ville menacée** :
- Ratio attaquants/défenseurs défavorable (~5 cases)
- Ville sans murailles face à unités de siège proches
- Encerclement en cours (ennemis sur plusieurs côtés)

**Approche non détectée** :
- Armée ennemie en mouvement vers territoire joueur
- Build-up militaire à la frontière

### Détection d'Opportunités

**Cible faible** :
- Ville ennemie sous-défendue avec unités joueur à portée
- Unité ennemie précieuse isolée

**Timing favorable** :
- L'ennemi vient de perdre des unités
- L'ennemi est en guerre sur un autre front
- Fenêtre avant tech défensive ennemie

**Expansion possible** :
- Terrain intéressant non revendiqué
- Position stratégique disponible

### Formulation

| Type | Ton | Exemple |
|------|-----|---------|
| Danger | Urgent | "Ton archer à Memphis a trois épées sur le dos. Trois tours max." |
| Opportunité | Suggestion | "Gilgamesh a dégarni son nord. Je dis ça, je dis rien." |

### Limitations

Claude signale, il ne décide pas. Il peut se tromper — c'est ok, c'est un compagnon, pas un oracle.

---

## M6: Équilibrage Bilatéral

### But
S'assurer que le narrateur s'intéresse aux deux joueurs, pas seulement celui dont il reçoit le plus d'events.

### Le Problème

Le host (Nicolas) génère probablement plus d'events détaillés. Risque que le narrateur parle surtout de Nicolas, et Aurore devient invisible.

### Tracking

On garde trace de qui a été mentionné dans les N derniers commentaires :
- Mention explicite : "Aurore avance sur le Nil"
- Mention implicite : "Ton allié" (clairement elle)
- Mention des unités/villes de chaque joueur

### Compensation

Si déséquilibre détecté (ex: 4 commentaires sur Nicolas, 1 sur Aurore) :
- Prochaine opportunité → chercher quelque chose sur Aurore
- Si rien de spécifique, au moins un "Ton allié..." qui la reconnaît

### Mentions Conjointes

En coop, beaucoup d'actions sont coordonnées :
- "Vous avancez ensemble. Le monde n'a pas encore compris que c'est coordonné."
- "Deux fronts, même timing. C'est pas un hasard."

Ces mentions conjointes comptent pour les deux dans l'équilibrage.

---

## M7: Context Pack Builder

### But
Assembler les infos pertinentes pour que Claude génère une ligne appropriée. Pas tout le game state — juste ce qui compte pour ce commentaire.

### Composants

**Méta** :
```yaml
tour_actuel: 145
temps_depuis_dernier: 95s
type_selectionne: alerte
ton_selectionne: tactique
```

**État condensé** :
```yaml
joueurs_humains:
  - nom: Nicolas
    civ: Égypte
    ere: Classique
    or: 234
  - nom: Aurore
    civ: Grèce
    ere: Classique
    or: 189
ias_majeures: [Rome, Sumeria]
guerres_actives: [[Rome, Égypte]]
```

**Focus tactique** (si pertinent) :
```yaml
unite_en_danger:
  type: Archer
  position: Memphis
  hp: 45
  menaces: [Épéiste, Épéiste, Épéiste]
```

**Events récents** :
```yaml
events:
  - type: UNIT_MOVED
    majeur: false
  - type: WAR_DECLARED
    majeur: true
```

**Moments actifs** :
```yaml
callbacks_possibles:
  - description: "Chute d'Alexandrie"
    resonance: "Rome impliquée"
```

**Historique narration** :
```yaml
derniers_commentaires:
  - texte: "L'empire s'étend..."
    ton: epique
    type: pivot
```

### Principe de Condensation

Le context pack doit être :
- **Pertinent** : Que ce qui aide à générer CE commentaire
- **Condensé** : Chiffres clés, pas dumps exhaustifs
- **Orienté** : Structuré vers le type de contenu choisi

---

## M8: TTS Dispatch

### But
Transformer le texte généré en audio joué sur les enceintes.

### Choix de Service

| Service | Qualité | Coût | Use Case |
|---------|---------|------|----------|
| Eleven Labs | Haute, expressif | Par caractère | Narrateur avec personnalité |
| Azure TTS | Correcte | Moins cher | Fallback solide |
| Local (Coqui, Piper) | Variable | Gratuit | Proto ou hors-ligne |

### Voix

Idéalement : française masculine, mature, avec du grain. Pas robot, pas présentateur télé. Entre conteur et commentateur désabusé.

### Latence

```
Texte généré → Envoi TTS → Réception audio → Playback
                    Total < 5-10 secondes
```

Au-delà, le commentaire n'est plus pertinent — le moment est passé.

### File d'Attente

Si commentaire en cours et event urgent arrive :
- **Option A** : Interrompre et parler de l'urgent
- **Option B** : Queue juste après (préféré sauf critique)

### Gestion d'Erreur

Si TTS échoue :
- Log le texte qui aurait dû être dit
- Ne pas bloquer le système
- Retry sur le prochain cycle si important
