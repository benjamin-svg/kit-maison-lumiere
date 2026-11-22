---
name: ticket-vers-merge-request
description: Mini usine logicielle locale - lit un ticket, vérifie que ses critères sont testables, crée une branche, planifie, code test d'abord par petites étapes, relit son propre diff, fait relire par le sous-agent relecteur, puis prépare la merge request. Suit les pratiques courantes du développement (critères vérifiables, test d'abord, petits changements, relecture). À utiliser pour traiter un ticket d'évolution du portail.
argument-hint: "[fichier du ticket]"
disable-model-invocation: true
---

# Du ticket à la merge request (en local)

Ticket : $ARGUMENTS (par exemple `projets/portail/tickets/T-101-filtre-famille-delais.md`).
Si le prénom de la personne n'est pas connu, le demander.

Rappel : sur GitLab, une **merge request** (MR, « requête de fusion » dans GitLab en français) propose de fusionner une branche dans `main` ;
elle porte une description, la liste des commits, le résultat des tests automatiques et la relecture.
Ici on prépare tout cela en local : seule la création sur le serveur manque.

Cette skill suit les pratiques courantes des équipes de développement : un ticket prêt avant de coder
(critères vérifiables), un test écrit avant le code et vu en échec, des changements petits et limités au
ticket, une relecture de son propre diff puis par un autre, et une fusion décidée par un humain.

## Étapes

1. **Lire** le ticket et le `CLAUDE.md` du projet. Reformuler le besoin et lister les critères d'acceptation.
   Chaque critère doit être **vérifiable** (« étant donné..., quand..., alors... »). Si un critère est flou ou
   manque (cas d'une liste vide, d'une valeur absente, d'une majuscule), proposer une formulation et la faire
   confirmer avant de coder.
2. **Partir d'un état propre** : `git status` doit être propre (sinon, demander quoi faire).
   Le dossier `travail/` n'est pas versionné : ce qui s'y trouve ne compte pas.
   Se placer sur `main`, puis créer la branche `ticket/<identifiant>-<mot-cle>` (par exemple `ticket/T-101-filtre-famille`).
3. **Planifier** : proposer un plan court (fichiers à modifier, tests à ajouter, critère par critère).
   Le changement le plus petit qui remplit le ticket : pas de réorganisation du code ni d'amélioration hors
   sujet (elles feront l'objet d'un autre ticket). **Attendre l'accord** de la personne avant de coder.
4. **Coder test d'abord**, critère par critère :
   - écrire le test du critère, le lancer, **le voir échouer** pour la bonne raison ;
   - écrire le code le plus simple qui le fait passer ;
   - relire et simplifier si besoin, tests toujours verts.
   Tester la règle elle-même par un test court, et la page ou l'API par un test du client HTTP.
   Le hook relance les tests après chaque modification d'un fichier Python : lire son résultat.
   Pour une page web : vérifier les paramètres reçus (valeur absente, inconnue, majuscules), et ne jamais
   insérer dans du HTML ou du SQL un texte venu de l'utilisateur sans l'échapper ou le passer en paramètre.
5. **Lancer tous les tests** : `uv run pytest -q` dans le dossier du projet. Tout doit passer.
   Si la commande, l'usage ou une règle du projet a changé, mettre à jour le `README.md` ou le `CLAUDE.md`.
6. **Commiter** par petits commits, chacun avec des tests verts, messages en français, au présent, avec
   l'identifiant du ticket (« Ajoute le filtre famille sur l'API (T-101) »).
7. **Relire son propre diff** (`git diff main...HEAD`) en entier : code de débogage oublié, fichier modifié par
   erreur, test existant modifié. Si le diff dépasse environ 400 lignes, proposer de découper la merge request.
   Puis **faire relire** : appeler le sous-agent `relecteur` en lui donnant le nom de la branche et le ticket.
   Traiter ses remarques bloquantes et « à corriger », puis relancer les tests et commiter.
8. **Préparer la merge request** : écrire `travail/<prénom>/merge-requests/<identifiant>.md` :

```markdown
# <Titre court> (<identifiant du ticket>)
Branche : ticket/... -> main
## Pourquoi
## Ce qui change
## Critères d'acceptation (critère | fait | test qui le prouve)
## Comment tester (commandes et pages à ouvrir)
## Résultat des tests
## Relecture (verdict du relecteur et suites données)
## Risques et retour arrière (ce qui pourrait casser ailleurs ; comment annuler : git revert du commit de fusion)
## Points d'attention
```

9. **Si la personne le demande et que `glab` est installé et connecté** (dépôt hébergé sur GitLab) : pousser la
   branche et ouvrir la merge request avec `glab mr create --title "..." --description "$(cat <fichier>)"
   --target-branch main`, en brouillon (`--draft`) si la personne n'a pas encore relu.
10. **Résumer** : la branche, les commits (`git log main..HEAD --oneline`), le résultat des tests,
   le verdict du relecteur, et le chemin du message de merge request. Ne pas fusionner dans `main` :
   la fusion est la décision d'un humain.
