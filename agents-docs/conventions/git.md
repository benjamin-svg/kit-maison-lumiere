# Conventions git

## Branches

- La branche principale est `main`. On n'y commite jamais directement : tout passe par une merge request.
- Une branche par ticket : `ticket/<identifiant>-<deux mots du nom du fichier du ticket>`.
  Exemple : le ticket `T-101-filtre-famille-delais.md` donne `ticket/T-101-filtre-famille`.
- Chaque branche a son dossier de travail (worktree) : `.worktrees/<identifiant>`.
- Une branche part toujours de la dernière version de `main` sur le dépôt distant.

## Commits

- Message en français, au présent, qui commence par un verbe, avec l'identifiant du ticket entre parenthèses.
  Exemple : « Ajoute le filtre par famille sur la page des délais (T-101) ».
- Un commit regroupe un changement cohérent. Pas de commit « wip » ou « corrections ».
- Jamais commités : les données (`donnees/brutes/`, `*.duckdb`), le dossier `travail/`, les mots de passe et
  les clés.

## Récupérer main dans sa branche

- Par une fusion (`git merge origin/main`), au moins une fois par jour : /sync-dev.
- Pas de `rebase` ni de `push --force` sur une branche déjà envoyée : d'autres personnes peuvent l'avoir
  récupérée, et la merge request perdrait l'historique de la relecture.
- En cas de conflit, la personne choisit. Claude explique les deux versions, il ne tranche pas seul.
