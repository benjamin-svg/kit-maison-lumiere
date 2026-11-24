---
name: ship-dev
description: Envoie le travail d'un ticket en relecture - relance tous les tests, fait relire la branche par le sous-agent relecteur et traite ses remarques, enregistre et envoie la branche comme /sync-dev, termine la description de la merge request ouverte par /start-dev, la passe « Prête à relire » et passe le ticket « En relecture ». Ne fusionne jamais. Version GitLab de /ship. Étape du cycle start-dev, développement, test-dev, sync-dev, verify, ship-dev, close-dev.
argument-hint: "[identifiant du ticket, facultatif]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(git status*), Bash(git diff*), Bash(git log*), Bash(git add*), Bash(git commit*), Bash(git fetch*), Bash(git merge*), Bash(git push*), Bash(git branch*), Bash(git remote*), Bash(git worktree list*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *), Bash(glab mr update*)
---

# Envoyer un ticket en relecture

Ticket : $ARGUMENTS (facultatif).

Pourquoi cette skill : la personne qui relit trouve tout au même endroit, présenté de la même façon à chaque
fois, et elle sait que le travail est fini (la merge request n'est plus un brouillon). La fusion reste sa
décision : cette skill s'arrête avant.

Le /ship d'Anthropic fait la même chose sur GitHub. Il n'est pas annoncé pour GitLab : cette skill le remplace.

## Étapes

1. **Lire les conventions** `agents-docs/conventions/gitlab.md` et `tests.md` (dossier principal du kit).
   Absentes : suivre cette skill.
2. **Trouver la branche du ticket**, comme dans /sync-dev : `git branch --show-current` doit commencer par
   `ticket/`. Sinon, aller dans `.worktrees/<identifiant>`. Sinon, demander. Relire le ticket
   (`projets/*/tickets/<identifiant>-*.md`), sa liste de critères, et la merge request
   (`.depot-distant/merge-requests/<identifiant>.md`, ouverte par /start-dev). Si elle est déjà « Prête à
   relire » ou « Fusionnée », le dire et demander s'il faut continuer.
3. **Relancer tous les tests** : `uv run pytest -q` dans le dossier du projet. Si un test échoue, s'arrêter
   et le dire. Ne jamais modifier un test existant pour le faire passer. Si un critère du ticket n'a pas de
   test, s'arrêter et proposer /test-dev.
4. **Faire relire** : appeler le sous-agent `relecteur` en lui donnant le nom de la branche, le chemin du
   ticket, et en lui demandant de comparer avec `origin/main` (`git diff origin/main` montre aussi ce qui
   n'est pas encore commité). Traiter ses remarques « bloquant » et « à corriger », en disant ce que tu changes,
   puis relancer les tests. Si une remarque change ce que demande le ticket, demander d'abord. Les
   « suggestions » ne sont pas appliquées : elles vont dans la merge request.
5. **Enregistrer et envoyer** : lire `.claude/skills/sync-dev/SKILL.md` et suivre ses étapes 3 à 8 (commit,
   récupération de main, conflit éventuel, tests, envoi, mise à jour de la merge request). Jamais `--force`.
6. **Terminer la description** de la merge request : vérifier que chaque critère a son test et son résultat,
   puis remplir « Relecture du sous-agent » (verdict, remarques traitées, suggestions laissées), « Comment
   tester » (commande pour lancer le projet, page à ouvrir, valeur à choisir, ce qu'a montré /verify s'il a
   été lancé) et « Risques et retour arrière » (ce qui pourrait casser ailleurs, et comment annuler :
   `git revert` du commit de fusion). Un critère qui ne se vérifie pas par un test : l'écrire ici, pour la
   personne qui relit.
7. **Passer la merge request « Prête à relire »** : `uv run python outils/merge_request.py prete <identifiant>`
   (sur un vrai GitLab : `glab mr update <branche> --ready`, qui retire le brouillon).
8. **Passer le ticket « En relecture »** sur le tableau :
   `uv run python outils/tableau.py <identifiant> "En relecture"` (sur Jira : la page du ticket).
9. **Ne pas fusionner**, ne pas supprimer le worktree. La personne qui relit fusionne : dans Claude Code, elle
   tape `! uv run python outils/merge_request.py fusionner <identifiant>` (sur GitLab, le bouton « Merge »).
   Ensuite, /close-dev fait le ménage.

## Ce que tu affiches à la fin

```
Ticket <identifiant> envoyé en relecture.
✓ Tests : <résultat de pytest>
✓ Relecture : <verdict> (<n> remarques traitées)
✓ Branche envoyée : ticket/<…> (<dernier commit>)
✓ Merge request prête à relire : .depot-distant/merge-requests/<identifiant>.md
✓ Tableau : <identifiant> en relecture
Je ne fusionne pas : c'est la décision de la personne qui relit. Après la fusion : /close-dev <identifiant>.
```

Si la personne qui relit demande des changements : les faire dans le worktree, puis /sync-dev (la merge
request reste prête à relire et se met à jour).
