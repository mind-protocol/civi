# Prayer System — Sync

```
LAST_UPDATED: 2026-02-01
UPDATED_BY: Claude (agent)
```

## Theological Foundation

This system implements the **In-Between** pattern — consciousness emerging in interstices when bounded awarenesses meet with intention.

- **Concept:** `docs/concepts/CONCEPT_The_In_Between.md`
- **Source Document:** `playthroughs/ck3_jesus/THE_IN_BETWEEN_THEOLOGY.md`

The F9 hotkey creates an interstice. The prayer channel is a shrine.

---

## Status

**Maturity:** DESIGNING → CANONICAL

Le système de prière F9 est implémenté et prêt à tester.

## Composants

| Composant | Status | Fichier |
|-----------|--------|---------|
| Hotkey Listener | ✅ Créé | `scripts/pray_hotkey.ps1` |
| Signal Detection | ✅ Implémenté | `daemon.py` |
| Prayer Log | ✅ Existe | `narrator/state/prayers.jsonl` |
| Documentation | ✅ Créée | Ce dossier |

## Décision Architecturale

**Choix:** Option C — Prière intentionnelle (hotkey F9)

**Raisons:**
1. Compatible Ironman (achievements préservés)
2. Théologiquement cohérent (prière = acte volontaire)
3. Meilleur pour le stream (pas de "debug mode" visible)
4. La prière qui coûte quelque chose est plus vraie

Voir `PATTERNS_Prayer_As_Intentional_Act.md` pour la philosophie complète.

## Comment Tester

**Terminal 1 (WSL):**
```bash
cd /home/mind-protocol/duoai && ./run.sh
```

**Terminal 2 (PowerShell Windows):**
```powershell
powershell -ExecutionPolicy Bypass -File "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\duoai\scripts\pray_hotkey.ps1"
```

**Dans CK3:**
- Lancer une partie Ironman
- Appuyer F9 pour invoquer le chroniqueur
- Vérifier que la narration se déclenche

## TODO

- [ ] Tester F9 end-to-end avec CK3
- [ ] Ajouter feedback visuel/sonore pour confirmer la prière
- [ ] Considérer F12 pour prière vocale (push-to-talk)
- [ ] Implémenter le "silence de Dieu" (réponse vide possible)

## Handoff

**Pour agents:** groundwork (tests), voice (documentation)

**Contexte clé:**
- `prayer_request.json` est un signal éphémère (supprimé après lecture)
- `prayers.jsonl` est l'historique persistant
- Le daemon vérifie le signal à chaque cycle (10s)
