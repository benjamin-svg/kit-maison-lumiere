# Conventions GitLab

## Merge request

- Une merge request par ticket, de la branche du ticket vers `main`.
- Ouverte **en brouillon** dès le début du ticket (/start-dev), pour que l'équipe voie le travail en cours.
  Elle reste en brouillon tant que le travail n'est pas prêt à être relu.
- Titre : le titre du ticket, puis l'identifiant entre parenthèses. Exemple : « Filtre par famille sur la
  page des délais (T-101) ».
- Description, toujours dans cet ordre : Ce qui change, Critères du ticket (chaque critère avec le test qui le
  prouve), Tests, Relecture du sous-agent, Comment tester, Risques et retour arrière.
- Mise à jour à chaque envoi de la branche (/sync-dev), terminée et passée « Prête à relire » par /ship-dev.

## Relecture et fusion

- Une personne autre que l'auteur relit. C'est elle qui fusionne, jamais Claude.
- On ne fusionne pas un brouillon, ni une branche dont les tests échouent, ni une branche en conflit avec
  `main` (il faut d'abord lancer /sync-dev).
- Fusion avec un commit de fusion (pas de « squash »), et suppression de la branche sur GitLab (case
  « Delete source branch »).

## CI

- Sur GitLab, la CI relance tous les tests à chaque envoi. Une CI rouge bloque la fusion.

## Dans le kit

- Le dépôt GitLab est simulé dans `.depot-distant/` (`outils/depot_distant.py`).
- Les merge requests sont des fichiers `.depot-distant/merge-requests/<identifiant>.md`, tenus par
  `uv run python outils/merge_request.py` (ouvrir, prete, et fusionner pour la personne qui relit).
- Sur un vrai GitLab : `glab mr create --draft`, `glab mr update <n> --description`, `glab mr update <n> --ready`,
  et le bouton « Merge ».
