---
name: close-dev
description: Fait le ménage après la fusion d'un ticket - vérifie que la branche est bien fusionnée dans main, supprime le worktree et la branche locale, efface les fichiers locaux créés pour le ticket (avec accord), met main à jour sur le poste et passe le ticket « Terminé ». Ne fait rien si la branche n'est pas fusionnée. Dernière étape du cycle start-dev, développement, test-dev, sync-dev, verify, ship-dev, close-dev.
argument-hint: "[identifiant du ticket, par exemple T-101]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git status*), Bash(git log*), Bash(git fetch*), Bash(git switch*), Bash(git pull*), Bash(git branch*), Bash(git merge-base*), Bash(git worktree*), Bash(git ls-remote*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *)
---

# Clore un ticket après la fusion

Ticket : $ARGUMENTS (un identifiant comme `T-101`). Si rien n'est donné, lister `git worktree list` et
demander lequel clore.

Pourquoi cette skill : une fois la merge request fusionnée par une personne, il reste un worktree, une branche
et parfois des fichiers d'essai sur le poste, et un ticket à ranger. Les laisser encombre le poste et fausse le
tableau des tickets que voit toute l'équipe.

Toutes les commandes git de cette skill se lancent depuis le **dossier principal du kit**
(`git rev-parse --path-format=absolute --git-common-dir`, puis son dossier parent), pas depuis le worktree
qu'on va supprimer.

## Étapes

1. **Retrouver la branche** : `git branch --list "ticket/<identifiant>-*"`. Aucune : le dire et s'arrêter.
2. **Vérifier que la fusion a eu lieu** : la merge request (`uv run python outils/merge_request.py`) doit être
   « Fusionnée ». Puis la preuve par git : `git fetch --prune origin`, puis
   `git merge-base --is-ancestor <branche> origin/main`.
   - Code de retour différent de 0 : la branche n'est pas (ou pas entièrement) dans `main` sur le dépôt
     distant. S'arrêter, montrer les commits manquants (`git log --oneline origin/main..<branche>`) et
     rappeler que la fusion se fait par la personne qui relit
     (`! uv run python outils/merge_request.py fusionner <identifiant>`). Ne rien supprimer.
3. **Vérifier qu'il ne reste rien dans le worktree** : `git -C .worktrees/<identifiant> status --short`.
   Une modification non enregistrée : la montrer et demander quoi en faire. Ne rien jeter sans accord.
4. **Supprimer le worktree** : `git worktree remove .worktrees/<identifiant>`. Jamais `--force` sans accord.
5. **Mettre main à jour sur le poste** : `git switch main`, puis `git pull --ff-only origin main`.
6. **Supprimer la branche locale** : `git branch -d <branche>`. Jamais `-D` : si git refuse, c'est qu'un
   commit n'est pas dans `main`, s'arrêter et le dire. Si la branche existe encore sur le dépôt distant
   (`git ls-remote --heads origin <branche>`), le signaler : sur GitLab, on la supprime en cochant « Delete
   source branch » au moment de la fusion (`merge_request.py fusionner` le fait dans le kit).
7. **Fichiers locaux créés pour le ticket** : chercher dans `travail/<prénom>/` les fichiers dont le nom
   contient l'identifiant, ainsi que les exports d'essai cités dans la merge request. La merge request reste
   sur le dépôt distant, comme trace. Montrer la liste et demander avant d'effacer. Rien trouvé : le dire.
8. **Passer le ticket « Terminé »** : `uv run python outils/tableau.py <identifiant> "Terminé"`
   (sur Jira : la page du ticket, si aucune règle ne le fait déjà à la fusion).
9. **Vérifier l'état final** : `git status --short` propre, `git worktree list` sans le ticket, et les tests du
   projet sur `main` : `uv run pytest -q` dans `projets/<projet>/`.

## Ce que tu affiches à la fin

```
Ticket <identifiant> clos.
✓ Branche fusionnée dans main sur le dépôt distant (GitLab).
✓ Worktree supprimé : .worktrees/<identifiant>
✓ main à jour sur le poste, tests : <résultat de pytest>
✓ Branche locale supprimée : ticket/<…>
✓ Fichiers locaux : <effacés, gardés, ou aucun>
✓ Tableau : <identifiant> terminé
```

Ne fusionne rien, ne modifie aucun fichier du projet.
