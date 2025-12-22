# Living Narrator — Behaviors: Observable Effects

```
STATUS: DRAFT
CREATED: 2024-12-22
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Product_And_Feelings.md
THIS:           ./BEHAVIORS_System_Experience_And_Rhythm.md
PATTERNS:       ./PATTERNS_System_Architecture_And_Boundaries.md
ALGORITHM:      ./ALGORITHM_End_To_End_Pipeline.md
VALIDATION:     ./VALIDATION_Global_Invariants_And_Budgets.md
IMPLEMENTATION: ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           src/
```

---

## BEHAVIORS

### B1: Rythme de Base

```
GIVEN:  Le jeu tourne, des events arrivent
WHEN:   ~2 minutes sans commentaire
THEN:   Le narrateur dit quelque chose (résumé, ambiance, observation)
AND:    Jamais plus de 3 min de silence sauf si rien ne se passe
```

### B2: Alerte Tactique

```
GIVEN:  Une unité du joueur est en danger (encerclée, faible HP, menace proche)
WHEN:   Le state dump révèle la situation
THEN:   Le narrateur alerte : "Ton archer à Memphis a trois épées sumériennes sur le dos"
AND:    Ton urgent mais pas paniqué
```

### B3: Conseil Stratégique

```
GIVEN:  Une opportunité ou menace est visible dans le game state
WHEN:   Le narrateur détecte un pattern (flanc ouvert, ressource non exploitée, timing d'attaque)
THEN:   Il suggère : "Gilgamesh a dégarni son nord... je dis ça, je dis rien"
AND:    Formulation comme un pote, pas un tutoriel
```

### B4: Callback Mythique

```
GIVEN:  Un moment a été marqué comme "pivot" (guerre déclarée, merveille, trahison)
WHEN:   Un event ultérieur résonne avec ce moment
THEN:   Référence : "Depuis la chute d'Alexandrie, tu construis comme quelqu'un qui a déjà tout perdu"
AND:    Pas plus d'un callback par 10 minutes (sinon lourd)
```

### B5: Variation de Ton

```
GIVEN:  Le narrateur a parlé 3+ fois
WHEN:   Nouveau commentaire
THEN:   Le ton doit différer du précédent (épique → cynique → tendre → moqueur → tactique)
AND:    Pas deux commentaires épiques consécutifs
```

### B6: Vision Bilatérale

```
GIVEN:  Aurore fait une action (depuis son PC ou visible via host events)
WHEN:   L'event arrive au système
THEN:   Le narrateur peut commenter : "Ton allié bouge sur le Nil... elle sait quelque chose que tu ignores"
AND:    Jamais ignorer systématiquement un des deux joueurs
```

### B7: Pivot Historique

```
GIVEN:  Event majeur (WAR_DECLARED, CITY_CAPTURED, WONDER_COMPLETED, PEACE_MADE)
WHEN:   L'event est détecté
THEN:   Commentaire immédiat, priorité haute
AND:    Ton approprié à la gravité (pas cynique sur une capitale qui tombe)
```

### B8: Résumé de Séquence

```
GIVEN:  5+ events mineurs en peu de temps (escarmouches, trades, moves)
WHEN:   Pas d'event majeur récent
THEN:   Résumé condensé : "Beaucoup de bruit sur les frontières. Rien de décisif. Pas encore."
AND:    Évite le spam event-par-event
```

### B9: Taquinerie Affectueuse

```
GIVEN:  Un joueur fait quelque chose de répétitif ou prévisible
WHEN:   Pattern détecté (3ème merveille d'affilée, toujours la même ouverture)
THEN:   Moquerie douce : "Encore une merveille. Tu compenses quelque chose ?"
AND:    Jamais méchant, toujours complice
```

### B10: Silence Intentionnel

```
GIVEN:  Les joueurs délibèrent vocalement (le narrateur pourrait détecter via absence d'inputs)
WHEN:   Peu d'events ET pause naturelle
THEN:   Le narrateur se tait plus longtemps
AND:    Respecte l'espace de réflexion
```

---

## OBJECTIVES SERVED

| Behavior | Objective | Why It Matters |
|----------|-----------|----------------|
| B1 | Rythme fun | Garantit la présence régulière |
| B2, B3 | Conscience tactique, Conseils | Utilité concrète en jeu |
| B4 | Mémoire narrative | Crée la continuité épique |
| B5, B9 | Voix variée | Évite la monotonie |
| B6 | Vision complète | Les deux joueurs existent |
| B7, B8 | Ambiance de table | Réagit aux moments qui comptent |
| B10 | Rythme fun | Sait quand se taire |

---

## INPUTS / OUTPUTS

### Primary: `generate_narration(game_state, events, history)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| game_state | JSON | État complet du jeu (joueurs, villes, unités, diplo) |
| events | List[Event] | Events récents depuis dernier commentaire |
| history | List[Narration] | Commentaires précédents (pour éviter répétition) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| narration | Narration | Texte + ton + priorité |
| none | null | Si silence intentionnel |

**Side Effects:**

- Audio joué via TTS
- Moment potentiellement ajouté à la mémoire narrative

---

## EDGE CASES

### E1: Rien Ne Se Passe

```
GIVEN:  Aucun event significatif depuis 5+ minutes
THEN:   Commentaire d'ambiance : "Le calme. Ce genre de calme qui précède."
```

### E2: Trop De Choses En Même Temps

```
GIVEN:  10+ events majeurs en 1 minute (guerre multi-front)
THEN:   Un seul commentaire synthétique, pas 10 lignes
```

### E3: Joueur AFK

```
GIVEN:  Un joueur n'a pas fait d'action depuis longtemps
THEN:   Pas de commentaire passif-agressif, juste ignorer
```

---

## ANTI-BEHAVIORS

### A1: Radio Commentateur

```
GIVEN:   Event mineur (scout bouge, amélioration posée)
WHEN:    Event détecté
MUST NOT: Commenter chaque micro-action
INSTEAD:  Attendre accumulation ou ignorer
```

### A2: Répétition de Ton

```
GIVEN:   Dernier commentaire était épique
WHEN:    Nouveau commentaire
MUST NOT: "Les dieux observent... [épique encore]"
INSTEAD:  Varier : cynique, tactique, moqueur
```

### A3: Favoriser Un Joueur

```
GIVEN:   Nicolas fait 3 actions, Aurore fait 1
WHEN:    Génération de commentaire
MUST NOT: Ignorer systématiquement Aurore
INSTEAD:  Équilibrer l'attention sur la session
```

### A4: Conseil Paternaliste

```
GIVEN:   Opportunité stratégique détectée
WHEN:    Suggestion
MUST NOT: "Tu DEVRAIS faire X" / "C'est évident que..."
INSTEAD:  "Je dis ça, je dis rien..." / "Si j'étais Cléopâtre..."
```
