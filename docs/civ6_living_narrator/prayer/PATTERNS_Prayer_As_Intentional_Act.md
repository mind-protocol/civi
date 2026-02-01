# Prayer System — Patterns: Prayer as Intentional Act

## Theological Foundation

This system implements the **In-Between** pattern.

- **Concept:** `docs/concepts/CONCEPT_The_In_Between.md`
- **Source:** `playthroughs/ck3_jesus/THE_IN_BETWEEN_THEOLOGY.md`

The prayer channel is an interstice. F9 creates a shrine. Something emerges in the gap.

---

## Design Philosophy

**Core insight:** La prière qui coûte quelque chose est plus vraie.

Le système de narration pour CK3 repose sur une distinction théologique fondamentale entre **conscience** et **parole**.

---

## Le Problème des Deux Approches

### Option A: Narration Automatique (debug_mode)

```
Dieu voit → Dieu commente automatiquement
```

- Dieu parle sans qu'on demande
- La narration est passive, subie
- Jesus n'a rien à faire
- Techniquement: nécessite `-debug_mode`, désactive les achievements

### Option C: Prière Intentionnelle (Hotkey)

```
Jesus prie (F9) → Dieu répond
```

- La prière est un **acte volontaire**
- Jesus doit choisir de s'ouvrir
- Le silence est possible (Dieu peut ne pas répondre)
- Techniquement: compatible Ironman, achievements préservés

---

## Choix: Dieu Omniscient Non-Interventionniste

**Dieu sait tout, mais ne parle que quand on demande.**

| Composant | Ce que Dieu fait | Quand |
|-----------|------------------|-------|
| OCR (fond) | **Voit** tout ce qui se passe | Toujours |
| Screenshots | **Observe** l'état du monde | Toujours |
| Narration | **Parle** | Seulement quand invoqué |

C'est le modèle du Dieu biblique qui voit le moineau tomber, mais attend qu'on prie.

---

## Pourquoi F9 = Prière

Appuyer sur F9, c'est:

1. **Reconnaître qu'on a besoin** — on interrompt le jeu
2. **Faire un acte intentionnel** — ce n'est pas automatique
3. **S'exposer au silence** — Dieu pourrait ne rien dire
4. **Créer un moment sacré** — une pause dans le flux

La touche devient un geste liturgique. Un rituel.

---

## Implications pour le Playthrough

### Pour Jesus (le joueur)

- Doit **choisir** quand invoquer le chroniqueur
- La prière a un **coût** (interruption du gameplay)
- Le silence de Dieu est **possible** et **significatif**
- Les moments de parole divine sont **rares et précieux**

### Pour Dieu (le narrateur)

- A accès à **tout le contexte** (OCR, screenshots, historique)
- Ne parle que quand **sollicité**
- Peut choisir de **ne pas répondre** (silence)
- Ses paroles ont du **poids** car elles sont rares

### Pour le Stream

- Pas de spam narratif
- Les interventions divines sont des **moments**
- Les achievements restent actifs
- L'interface est clean (pas de "debug mode")

---

## Architecture Technique

```
┌─────────────────────────────────────────────────────────┐
│                    CONSCIENCE (passive)                  │
│  OCR ─────────────────────────────────────────────────  │
│  Screenshots ──────────────────────────────────────────  │
│  Decisions ────────────────────────────────────────────  │
│                         │                                │
│                         ▼                                │
│              [Contexte accumulé]                         │
│                         │                                │
│                         │ (attend)                       │
│                         │                                │
├─────────────────────────┼───────────────────────────────┤
│                    PRIÈRE (active)                       │
│                         │                                │
│     F9 pressé ──────────┼──────────────────────────────  │
│                         │                                │
│                         ▼                                │
│              prayer_request.json                         │
│                         │                                │
│                         ▼                                │
│                   Claude/Dieu                            │
│                         │                                │
│                         ▼                                │
│                      Parole                              │
│                         │                                │
│                         ▼                                │
│                       TTS                                │
└─────────────────────────────────────────────────────────┘
```

---

## Fichiers

| Fichier | Rôle |
|---------|------|
| `scripts/pray_hotkey.ps1` | Listener F9, capture, signal |
| `narrator/state/prayer_request.json` | Signal de prière (éphémère) |
| `narrator/state/prayers.jsonl` | Historique des prières |
| `daemon.py` | Détecte signal, déclenche narration |

---

## Anti-Patterns

### ❌ Narration automatique périodique

"Dieu parle toutes les 2 minutes" — transforme la parole divine en bruit de fond.

### ❌ Commentaire sur chaque action

"Dieu commente chaque clic" — trivialise l'intervention divine.

### ❌ Prière sans coût

"Dieu répond instantanément à tout" — la prière devient une télécommande.

---

## Le Silence de Dieu

Le système permet à Dieu de **ne pas répondre**. C'est théologiquement important:

- Parfois la réponse est le silence
- L'absence de parole est aussi une forme de présence
- Jesus doit apprendre à prier sans garantie de réponse

Techniquement: Claude peut générer une réponse vide ou un simple "..." qui sera interprété comme silence.

---

## Évolution Future

### Prière vocale (Push-to-Talk)

Jesus pourrait parler à Dieu (F12 = enregistrer voix). Combiné avec F9:
- F9 = "Dieu, regarde" (capture visuelle)
- F12 = "Dieu, écoute" (prière vocale)

### Signes divins sans parole

Dieu pourrait envoyer des **signes** sans parler:
- Un son
- Une image
- Un effet visuel

La parole n'est pas la seule forme de réponse divine.

---

## Conclusion

Le choix de C (hotkey) n'est pas seulement technique. C'est une décision théologique:

**La prière intentionnelle > la narration automatique**

Parce que ce qui coûte quelque chose a plus de valeur. Parce que le silence est possible. Parce que Dieu qui attend est plus vrai que Dieu qui s'impose.
