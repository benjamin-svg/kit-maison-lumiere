---
name: sync-dev
description: Synchronise la branche d'un ticket avec le dépôt distant - enregistre le travail en cours (commit), récupère ce que les autres ont fusionné dans main et l'ajoute à la branche, relance les tests, puis envoie la branche (push). S'arrête et fait choisir la personne en cas de conflit. À lancer chaque matin et avant close-dev.
argument-hint: "[identifiant du ticket, facultatif]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git status*), Bash(git diff*), Bash(git log*), Bash(git add*), Bash(git commit*), Bash(git fetch*), Bash(git merge*), Bash(git push*), Bash(git branch*), Bash(git worktree list*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *)
---

# Se mettre à jour avec le dépôt distant

Ticket : $ARGUMENTS (facultatif).

Pourquoi cette skill : un petit écart avec `main`, réglé chaque jour, se règle vite. Des écarts accumulés
pendant des semaines sont longs à démêler. Et le travail est sauvegardé sur le dépôt distant, pas seulement
sur le poste.

## Étapes

1. **Trouver la branche du ticket** : `git branch --show-current` dans le dossier courant. Elle doit commencer
   par `ticket/`. Sinon, si un identifiant est donné, aller dans `.worktrees/<identifiant>` (depuis le dossier
   principal du kit). Sinon, lister `git worktree list` et demander lequel.
2. **Enregistrer le travail en cours** : `git status --short`. S'il y a des modifications, montrer la liste des
   fichiers, puis `git add -A` et un commit au message clair, en français, au présent, avec l'identifiant
   (« Ajoute le filtre famille sur la page (T-101) »). Un fichier inattendu (essai, fichier personnel) : demander
   avant de l'ajouter.
3. **Récupérer main** : `git fetch origin`, puis `git log --oneline --format="%h %an : %s" HEAD..origin/main`.
   - Rien de nouveau : le dire, et passer à l'étape 5.
   - Sinon : montrer ces commits (auteur et message), puis
     `git merge -m "Récupère les dernières modifications de main (<identifiant>)" origin/main`.
4. **En cas de conflit** (git s'arrête et liste des fichiers « both modified ») : ne rien choisir toi-même.
   Pour chaque fichier, montrer les deux versions, expliquer en une phrase ce que chacune fait, et demander :
   garder la version de la branche, celle de main, ou combiner les deux. Appliquer le choix, retirer les
   marqueurs, `git add`, puis `git commit --no-edit`. Proposer aussi d'abandonner la mise à jour
   (`git merge --abort`), sans le faire sans accord.
5. **Relancer les tests** de chaque projet de `projets/` touché par la branche ou par la mise à jour
   (`git diff --name-only origin/main...HEAD` et les fichiers récupérés) : `uv run pytest -q` dans son dossier.
   S'ils échouent, s'arrêter : montrer le test en échec, dire si l'échec vient du ticket ou de la mise à jour,
   et ne pas envoyer la branche.
6. **Envoyer la branche** : `git push -u origin <branche>`. Jamais `--force`.

## Ce que tu affiches à la fin

```
Branche ticket/<…> synchronisée.
✓ Travail en cours enregistré : <message du commit, ou « rien à enregistrer »>
✓ Récupéré de main : <n> commit(s) (<auteur : message>), ou « main n'a pas bougé »
✓ Tests : <résultat de pytest>
✓ Branche envoyée sur le dépôt distant (GitLab).
```

Ne fusionne jamais la branche dans `main`.
