# Living Narrator — Validation: Invariants and Tests (v2)

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
THIS:           ./VALIDATION_Global_Invariants_And_Budgets.md
IMPLEMENTATION: ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           src/
```

---

## BEHAVIORS GUARANTEED

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|------------------------------|
| B1 | Rythme de base | V1 garantit qu'on parle dans les temps |
| B5 | Variation de ton | V2 garantit qu'on ne répète pas |
| B6 | Vision bilatérale | V3 garantit l'équilibre |
| B7 | Pivot historique | V4 garantit qu'on marque les grands moments |

---

## OBJECTIVES COVERED

| Objective | Validations | Rationale |
|-----------|-------------|-----------|
| Rythme fun | V1, V5 | Timing respecté, pas de spam |
| Voix variée | V2 | Rotation de ton |
| Vision complète | V3 | Deux joueurs existent |
| Ambiance de table | V4, V6 | Pivots célébrés, audio fonctionne |
| Conseils bienvenus | V7 | Le narrateur a des opinions |

---

## INVARIANTS

### V1: Fenêtre de Timing

```
Le narrateur parle au moins une fois toutes les 3 minutes
ET jamais plus d'une fois par 30 secondes
```

**Checked by:** Timer entre narrations

### V2: Non-Répétition de Ton

```
Deux narrations consécutives n'ont JAMAIS le même ton
```

**Checked by:** Comparaison historique avant génération

### V3: Équilibre Bilatéral

```
Sur 10 commentaires, chaque joueur humain est mentionné au moins 2 fois
```

**Checked by:** Compteur de mentions

### V4: Pivots Célébrés

```
Les events majeurs (guerre, chute de ville, élimination)
déclenchent une narration riche — le narrateur peut :
- Prendre son temps (3-4 phrases au lieu de 1-2)
- Inventer des détails narratifs (météo, ambiance, ce que "les chroniqueurs diront")
- Être dramatique, partial, émotif
```

**Checked by:** Vérification que les pivots génèrent des narrations plus longues

### V5: Pas de Spam

```
Maximum 2 narrations par minute, même avec events multiples
```

**Checked by:** Rate limiter

### V6: Audio Fonctionnel

```
Chaque narration générée produit un audio joué
OU une erreur loggée
```

**Checked by:** Callback playback

### V7: Personnalité Assumée

```
Le narrateur PEUT :
- Donner son avis ("j'aurais pas fait ça")
- Proposer des challenges ("et si tu prenais cette ville en 10 tours ?")
- Critiquer gentiment ("encore cette stratégie ?")
- Prendre parti ("je suis team Aurore sur ce coup")
- Spéculer ("je sens que Gilgamesh prépare quelque chose")

Ces comportements sont AUTORISÉS, pas obligatoires.
```

**Checked by:** Revue qualitative des logs

---

## PROPERTIES

### P1: Variation sur Longue Durée

```
FORALL fenêtre de 10 narrations:
    Au moins 4 tons différents utilisés
```

**Verified by:** Analyse historique post-session

### P2: Distribution de Types

```
FORALL session > 1 heure:
    Au moins 4 types de contenu différents
    (pivot, conseil, callback, taquinerie, ambient, challenge...)
```

**Verified by:** Stats de session

### P3: Richesse des Pivots

```
FORALL narration sur event majeur:
    Longueur >= 2x longueur moyenne
    OU contient détail inventé/narratif
```

**Verified by:** Analyse longueur + contenu

### P4: Challenges Proposés

```
FORALL session > 2 heures:
    Au moins 1 challenge proposé par le narrateur
    ("Et si...", "Je te défie de...", "Tu penses pouvoir...")
```

**Verified by:** Détection pattern dans les narrations

---

## ERROR CONDITIONS

### E1: TTS Timeout

```
WHEN:    TTS ne répond pas en 10 secondes
THEN:    Log, skip, continue
SYMPTOM: Silence ponctuel
```

### E2: Game State Stale

```
WHEN:    game_state.json pas mis à jour depuis > 60s
THEN:    Mode ambient only, log warning
SYMPTOM: Commentaires génériques
```

### E3: Claude API Failure

```
WHEN:    Claude ne répond pas
THEN:    Retry 1x, puis skip
SYMPTOM: Gap dans les narrations
```

### E4: Event Buffer Overflow

```
WHEN:    > 50 events non traités
THEN:    Résumé condensé, clear buffer
SYMPTOM: Un commentaire de synthèse
```

---

## CE QUE LE NARRATEUR DÉCIDE SEUL

Pas de validation rigide sur :

- **Quand alerter sur un danger** — il voit le state, il juge
- **Quand faire un callback** — il sent la résonance
- **Quand taquiner** — il lit le pattern
- **Quand donner un conseil** — il voit l'opportunité
- **Quand proposer un challenge** — il sent le moment
- **Quand critiquer** — il a une opinion

Le narrateur est un compagnon avec du jugement. On valide le cadre (timing, variation, équilibre), pas chaque décision.

---

## VALIDATION COVERAGE

| Invariant | Status |
|-----------|--------|
| V1: Timing | ⚠ À IMPLÉMENTER |
| V2: Non-répétition ton | ⚠ À IMPLÉMENTER |
| V3: Équilibre bilatéral | ⚠ À IMPLÉMENTER |
| V4: Pivots célébrés | ⚠ À IMPLÉMENTER |
| V5: Pas de spam | ⚠ À IMPLÉMENTER |
| V6: Audio fonctionnel | ⚠ À IMPLÉMENTER |
| V7: Personnalité assumée | REVUE QUALITATIVE |

---

## VERIFICATION PROCEDURE

### Manuel (partie test)

```
[ ] Le narrateur parle toutes les ~2 min
[ ] Jamais deux fois le même ton d'affilée
[ ] Les deux joueurs sont mentionnés
[ ] Les pivots sont marqués avec emphase
[ ] Le narrateur donne parfois son avis
[ ] Le narrateur propose parfois des challenges
[ ] L'audio joue
```

### Post-session

```bash
python scripts/validate_session.py logs/session.jsonl
```

---

## MARKERS

<!-- @ngram:todo Implémenter analyse de richesse des pivots -->
<!-- @ngram:todo Détecter les patterns de challenge dans les narrations -->
<!-- @ngram:proposition Tracker quand le narrateur "prend parti" et si ça plaît -->
