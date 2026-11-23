---
paths:
  - "**/*.sql"
---

# Règles pour les fichiers SQL

Cette règle n'est lue que quand un fichier `.sql` est ouvert. Elle complète `CLAUDE.md` sans le répéter.

- Avant d'écrire ou de modifier une requête, relire la définition de la métrique dans
  `semantique/metriques.yml` et la fiche de chaque table utilisée. Ne pas recopier la définition ici.
- En tête du fichier, un commentaire dit la question posée, la période et la métrique utilisée.
- Écrire les dates au format AAAA-MM-JJ (`DATE '2025-12-01'`), et les bornes de période en clair.
- Après une jointure, compter les lignes avant et après : un nombre qui augmente signale des doublons.
- Lancer la requête avec `uv run python outils/requete.py -f <fichier>` avant de citer un chiffre.
