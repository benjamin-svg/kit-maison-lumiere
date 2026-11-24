# Documentation pour les agents

Ce dossier décrit les règles de l'équipe que Claude doit suivre quand il travaille sur ce dépôt.
Les skills du cycle d'un ticket (/start-dev, /test-dev, /sync-dev, /ship-dev, /close-dev) lisent
`conventions/` avant d'agir.

Pourquoi un dossier à part, et pas tout dans `CLAUDE.md` : `CLAUDE.md` est lu à chaque session, en entier.
Ces règles ne servent qu'au moment d'une action précise (créer une branche, écrire un test, ouvrir une merge
request) : chaque skill lit seulement le fichier dont elle a besoin. Un fichier par sujet se relit et se
corrige facilement, par la personne qui connaît le sujet.

| Fichier | Sujet | Lu par |
|---|---|---|
| `conventions/git.md` | branches, commits, récupération de main | /start-dev, /sync-dev, /ship-dev, /close-dev |
| `conventions/gitlab.md` | merge requests, relecture, fusion, CI | /start-dev, /sync-dev, /ship-dev |
| `conventions/tests.md` | où sont les tests, comment les lancer et les écrire | /start-dev, /test-dev, /sync-dev, /ship-dev |
| `conventions/jira.md` | tickets : identifiant, contenu, colonnes du tableau | /start-dev, /ship-dev, /close-dev |

Créé et mis à jour par `/setup-agents-doc`. Ces fichiers se modifient comme du code : par une merge request,
relue par l'équipe.
