---
name: close-dev
description: Termine le travail sur un ticket - relance tous les tests, fait relire la branche par le sous-agent relecteur et traite ses remarques, fait le dernier commit, envoie la branche, puis prépare la merge request avec sa description. Ne fusionne jamais. Dernière étape du cycle start-dev, sync-dev, close-dev.
argument-hint: "[identifiant du ticket, facultatif]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Bash(git status*), Bash(git diff*), Bash(git log*), Bash(git add*), Bash(git commit*), Bash(git fetch*), Bash(git merge*), Bash(git push*), Bash(git branch*), Bash(git remote*), Bash(git worktree list*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *), Bash(glab mr create*)
---

# Terminer un ticket

Ticket : $ARGUMENTS (facultatif). Si le prénom de la personne n'est pas connu, le demander.

Pourquoi cette skill : la personne qui relit trouve tout au même endroit, présenté de la même façon à chaque
fois. La fusion reste la décision d'une personne : cette skill s'arrête à la merge request.

## Étapes

1. **Trouver la branche du ticket**, comme dans /sync-dev : `git branch --show-current` doit commencer par
   `ticket/`. Sinon, aller dans `.worktrees/<identifiant>`. Sinon, demander. Relire le ticket
   (`projets/*/tickets/<identifiant>-*.md`) et sa liste de critères.
2. **Relancer toutes les vérifications** : `uv run pytest -q` dans le dossier du projet. Si un test échoue,
   s'arrêter et le dire. Ne jamais modifier un test existant pour le faire passer.
3. **Faire relire** : appeler le sous-agent `relecteur` en lui donnant le nom de la branche, le chemin du
   ticket, et en lui demandant de comparer avec `origin/main` (`git diff origin/main` montre aussi ce qui
   n'est pas encore commité). Traiter ses remarques « bloquant » et « à corriger », en disant ce que tu changes,
   puis relancer les tests. Si une remarque change ce que demande le ticket, demander d'abord. Les
   « suggestions » ne sont pas appliquées : elles vont dans la merge request.
4. **Faire le dernier commit** : `git add -A`, puis un commit au message clair, en français, au présent,
   avec l'identifiant (« Ajoute le filtre par famille (T-101) »). Rien à commiter : passer à la suite.
5. **Se mettre à jour, puis envoyer** : `git fetch origin`. Si `origin/main` a des commits que la branche n'a
   pas, faire d'abord les étapes 3 à 5 de /sync-dev (fusion de `origin/main`, conflit éventuel, tests).
   Puis `git push -u origin <branche>`. Jamais `--force`.
6. **Préparer la merge request** : écrire la description dans le dossier principal du kit (pas dans le
   worktree, qui sera supprimé) : `travail/<prénom>/merge-requests/<identifiant>.md`.

```markdown
# <Titre court> (<identifiant>)
Branche : ticket/<…> → main

## Ce qui change
## Critères du ticket
| Critère | Vérification qui le prouve (fichier et nom du test) | Résultat |
## Vérifications
(résultat de pytest : nombre de tests, tous réussis)
## Relecture du sous-agent
(verdict, remarques traitées, suggestions laissées)
## Comment tester
(commande pour lancer le projet, page à ouvrir, valeur à choisir)
## Risques et retour arrière
(ce qui pourrait casser ailleurs, et comment annuler : git revert du commit de fusion)
```

   Si le dépôt distant est un vrai GitLab et que `glab` est installé et connecté, ouvrir aussi la merge request
   en brouillon : `glab mr create --draft --source-branch <branche> --target-branch main --title "<titre>"
   --description "$(cat <fichier>)"`. Sinon, le fichier tient lieu de merge request.
7. **Ne pas fusionner**, ne pas supprimer le worktree. Après la fusion par une personne, le worktree se
   supprime avec `git worktree remove .worktrees/<identifiant>`.

## Ce que tu affiches à la fin

```
Ticket <identifiant> terminé, prêt pour la relecture.
✓ Vérifications : <résultat de pytest>
✓ Relecture : <verdict> (<n> remarques traitées)
✓ Dernier commit : <message>
✓ Branche envoyée : ticket/<…>
✓ Merge request : travail/<prénom>/merge-requests/<identifiant>.md
Je ne fusionne pas : c'est la décision de la personne qui relit.
```
