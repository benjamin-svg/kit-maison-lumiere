# Modèle pour analyser BigQuery avec Claude Code

Fichiers à copier dans votre dépôt d'analyses lundi. Le mode d'emploi complet est dans `lundi/bigquery.md`.

| Fichier du modèle | Dans votre dépôt |
|---|---|
| `CLAUDE.modele.md` | `CLAUDE.md` (à remplir : projet, tables, partitions) |
| `claude/settings.json` | `.claude/settings.json` |
| `claude/hooks/garde_cout_bq.py` | `.claude/hooks/garde_cout_bq.py` |
| `claude/skills/analyse-bigquery/` | `.claude/skills/analyse-bigquery/` |
| `../../semantique/` (du kit) | `semantique/` : la structure, à remplir avec vos vraies tables |

Vérifier le garde-fou sans BigQuery : `python3 tester_garde_cout.py` (« Tous les cas sont conformes. »).

Sous Windows, remplacez `python3` par `python` dans `settings.json`.
