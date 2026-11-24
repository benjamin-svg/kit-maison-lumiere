---
name: start-dev
description: Démarre le travail sur un ticket - lit le ticket, met main à jour depuis le dépôt distant, crée la branche ticket/<identifiant>-<mot-clé> et un worktree (une copie de travail dans .worktrees/<identifiant>), vérifie que les tests passent au départ. Ne code rien. Première étape du cycle start-dev, sync-dev, close-dev.
argument-hint: "[identifiant du ticket, par exemple T-101]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git status*), Bash(git switch*), Bash(git pull*), Bash(git fetch*), Bash(git branch*), Bash(git worktree*), Bash(git remote*), Bash(git log*), Bash(git rev-parse*), Bash(uv run *), Bash(ln -s *), Bash(cd *)
---

# Démarrer un ticket

Ticket : $ARGUMENTS (un identifiant comme `T-101`). Si rien n'est donné, liste les tickets de
`projets/*/tickets/` avec leur titre et demande lequel traiter.

Pourquoi cette skill : chaque demande part de la dernière version de `main`, a sa propre branche et son propre
dossier, et suit toujours la même règle de nommage. Les autres travaux en cours ne sont pas touchés.

Toutes les commandes git de cette skill se lancent depuis le **dossier principal du kit**
(`git rev-parse --path-format=absolute --git-common-dir`, puis son dossier parent), pas depuis un worktree.

## Étapes

1. **Lire le ticket** : `projets/*/tickets/<identifiant>-*.md`. Le résumer en une phrase et compter ses
   critères d'acceptation. Si un critère n'est pas vérifiable, le signaler (sans bloquer : on en reparlera
   au moment du plan).
2. **Vérifier le dépôt distant** : `git remote get-url origin`.
   - Pas de dépôt distant : lancer `uv run python outils/depot_distant.py`, qui crée le dépôt distant
     du kit (il joue le rôle de GitLab), et le dire en une phrase.
   - Si le script refuse (le kit a déjà un autre dépôt distant), s'arrêter et répéter son message.
3. **Partir d'un état propre** : `git status --short` dans le dossier principal. Le dossier `travail/` n'est pas
   suivi et ne compte pas. S'il reste des modifications, les montrer et demander quoi faire. Ne rien jeter.
4. **Mettre main à jour** : `git switch main`, puis `git pull --ff-only origin main`.
5. **Choisir le nom de la branche** : `ticket/<identifiant>-<les deux premiers mots du nom du fichier du ticket>`.
   Exemple : `T-101-filtre-famille-delais.md` donne `ticket/T-101-filtre-famille`.
   Si la branche existe déjà et a son worktree dans `.worktrees/<identifiant>`, reprendre ce dossier et le dire.
   Si elle existe sans worktree, demander s'il faut la reprendre.
6. **Créer la branche et le worktree** :
   `git worktree add -b ticket/<identifiant>-<mots> .worktrees/<identifiant>`.
   Le dossier `.worktrees/` est ignoré par git.
7. **Donner accès à la base** au worktree (elle n'est pas versionnée) : si `donnees/ecommerce.duckdb` existe
   dans le dossier principal, créer le lien
   `ln -s ../../../donnees/ecommerce.duckdb .worktrees/<identifiant>/donnees/ecommerce.duckdb`.
8. **Vérifier le point de départ** : dans `.worktrees/<identifiant>/projets/<projet du ticket>/`, lancer
   `uv run pytest -q` (la première fois, uv prépare l'environnement du worktree, quelques secondes).
   Tout doit passer. Sinon, s'arrêter et le dire : le problème existait avant le ticket.
9. **Se placer dans le worktree** : `cd .worktrees/<identifiant>`. Pour toute la suite de la session, lire et
   modifier les fichiers **de ce dossier**, pas ceux du dossier principal.

## Ce que tu affiches à la fin

```
Ticket <identifiant> : <résumé en une phrase>. <n> critères.
✓ main est à jour avec le dépôt distant (GitLab).
✓ Branche créée : ticket/<identifiant>-<mots>
✓ Worktree créé : dossier .worktrees/<identifiant>
✓ Tests au départ : <résultat de pytest>
Je travaille maintenant dans ce dossier.
```

Puis, en une ligne, les trois commandes git lancées, et la suite : « Demande-moi de traiter le ticket.
Je te présenterai d'abord mon plan. »

Ne code rien dans cette skill. Ne fusionne rien.
