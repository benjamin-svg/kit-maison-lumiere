---
name: sync-dev
description: Synchronise la branche d'un ticket avec le dépôt distant et met à jour sa merge request - enregistre le travail en cours (commit), récupère ce que les autres ont fusionné dans main, relance les tests, envoie la branche (push), puis met à jour la description de la merge request ouverte par /start-dev. Ne change pas son statut. S'arrête et fait choisir la personne en cas de conflit. À lancer après /test-dev, chaque matin, et dès qu'on veut montrer son travail. Étape du cycle start-dev, développement, test-dev, sync-dev, verify, ship-dev, close-dev.
argument-hint: "[identifiant du ticket, facultatif]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(git status*), Bash(git diff*), Bash(git log*), Bash(git add*), Bash(git commit*), Bash(git fetch*), Bash(git merge*), Bash(git push*), Bash(git branch*), Bash(git worktree list*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *), Bash(glab mr update*)
---

# Envoyer son travail et mettre à jour la merge request

Ticket : $ARGUMENTS (facultatif).

Pourquoi cette skill : le travail est sauvegardé sur le dépôt distant, pas seulement sur le poste, et la merge
request montre à l'équipe où en est le ticket. Récupérer `main` souvent évite les gros conflits : un petit
écart réglé chaque jour se règle vite, des écarts accumulés pendant des semaines sont longs à démêler.

## Étapes

1. **Lire les conventions** `agents-docs/conventions/git.md`, `gitlab.md` et `tests.md` (dossier principal du
   kit). Elles priment sur les exemples de cette skill. Absentes : suivre cette skill.
2. **Trouver la branche du ticket** : `git branch --show-current` dans le dossier courant. Elle doit commencer
   par `ticket/`. Sinon, si un identifiant est donné, aller dans `.worktrees/<identifiant>` (depuis le dossier
   principal du kit). Sinon, lister `git worktree list` et demander lequel.
3. **Enregistrer le travail en cours** : `git status --short`. S'il y a des modifications, montrer la liste des
   fichiers, puis `git add -A` et un commit au format de `git.md` (sans convention : en français, au présent,
   avec l'identifiant : « Ajoute le filtre famille sur la page (T-101) »). Un fichier inattendu (essai,
   fichier personnel) : demander avant de l'ajouter.
4. **Récupérer main** : `git fetch origin`, puis `git log --oneline --format="%h %an : %s" HEAD..origin/main`.
   - Rien de nouveau : le dire, et passer à l'étape 6.
   - Sinon : montrer ces commits (auteur et message), puis
     `git merge -m "Récupère les dernières modifications de main (<identifiant>)" origin/main`.
5. **En cas de conflit** (git s'arrête et liste des fichiers « both modified ») : ne rien choisir toi-même.
   Pour chaque fichier, montrer les deux versions, expliquer en une phrase ce que chacune fait, et demander :
   garder la version de la branche, celle de main, ou combiner les deux. Appliquer le choix, retirer les
   marqueurs, `git add`, puis `git commit --no-edit`. Proposer aussi d'abandonner la mise à jour
   (`git merge --abort`), sans le faire sans accord.
6. **Relancer les tests** de chaque projet de `projets/` touché par la branche ou par la mise à jour
   (`git diff --name-only origin/main...HEAD` et les fichiers récupérés) : `uv run pytest -q` dans son dossier.
   S'ils échouent, s'arrêter : montrer le test en échec, dire si l'échec vient du ticket ou de la mise à jour,
   et ne pas envoyer la branche.
7. **Envoyer la branche** : `git push -u origin <branche>`. Jamais `--force`.
8. **Mettre à jour la merge request** : le fichier `.depot-distant/merge-requests/<identifiant>.md` du dossier
   principal du kit. S'il n'existe pas, l'ouvrir comme à l'étape 11 de /start-dev
   (`uv run python outils/merge_request.py ouvrir ...`). Modifier seulement :
   - « Ce qui change » : en quelques phrases, ce que fait la branche, puis la liste des commits
     (`git log --oneline origin/main..HEAD`) et des fichiers modifiés (`git diff --stat origin/main...HEAD`) ;
   - « Critères du ticket » : pour chaque critère, le test qui le prouve et son résultat, repris de /test-dev
     s'il a été lancé. Sinon, ne pas deviner : laisser « à vérifier par /test-dev » ;
   - « Tests » : le résultat de l'étape 6, avec la date.
   Ne pas toucher au statut (brouillon, ou prête à relire si /ship-dev est déjà passé), ni aux parties
   remplies par /ship-dev.
   Sur un vrai GitLab : `glab mr update <branche> --description "$(cat <fichier>)"`.

## Ce que tu affiches à la fin

```
Branche ticket/<…> synchronisée.
✓ Travail en cours enregistré : <message du commit, ou « rien à enregistrer »>
✓ Récupéré de main : <n> commit(s) (<auteur : message>), ou « main n'a pas bougé »
✓ Tests : <résultat de pytest>
✓ Branche envoyée sur le dépôt distant (GitLab)
✓ Merge request mise à jour (<statut>) : <n> critères prouvés par un test sur <total>
```

Puis la suite : si la merge request est en brouillon, « /verify pour voir le résultat dans le portail, puis
/ship-dev quand le travail est prêt à être relu ». Si elle est déjà prête à relire, « La personne qui relit
voit tes changements dans la merge request. »

Ne fusionne jamais la branche dans `main`. Ne passe pas la merge request « Prête à relire » : c'est /ship-dev.
