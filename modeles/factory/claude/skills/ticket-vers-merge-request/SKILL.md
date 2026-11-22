---
name: ticket-vers-merge-request
description: Traite un ticket de bout en bout selon les pratiques courantes du développement - critères vérifiables, branche, plan validé, test d'abord, petits changements, relecture de son diff puis par le sous-agent relecteur, merge request (fichier local, ou vraie merge request GitLab avec glab). À utiliser pour une évolution ou une anomalie décrite dans un ticket.
argument-hint: "[fichier du ticket ou numéro de ticket GitLab]"
disable-model-invocation: true
---

# Du ticket à la merge request

Ticket : $ARGUMENTS. Un fichier de `tickets/`, ou un numéro de ticket GitLab (`glab issue view <n>`).

## Étapes

1. **Lire** le ticket et le `CLAUDE.md` du projet. Reformuler le besoin et lister les critères d'acceptation.
   Chaque critère doit être **vérifiable** (« étant donné..., quand..., alors... ») ; s'il est flou ou manque
   (liste vide, valeur absente), proposer une formulation et la faire confirmer avant de coder.
   S'il manque une information pour décider (une définition, une règle métier), s'arrêter et demander.
2. **Partir d'un état propre** : `git status` propre, puis `git switch main`, `git pull` si un dépôt distant
   existe, et `git switch -c ticket/<identifiant>-<mot-cle>`.
3. **Planifier** : fichiers à modifier, tests à ajouter, critère par critère. Le changement le plus petit
   qui remplit le ticket, sans amélioration hors sujet. **Attendre l'accord.**
4. **Coder test d'abord**, critère par critère : écrire le test, le voir échouer pour la bonne raison, écrire
   le code le plus simple qui le fait passer, puis simplifier, tests toujours verts. Pour une anomalie :
   d'abord un test qui la reproduit et échoue. Vérifier les paramètres reçus ; ne jamais insérer dans du HTML
   ou du SQL un texte venu de l'utilisateur sans l'échapper ou le passer en paramètre.
   Le hook relance les tests après chaque modification : lire son résultat.
   Ne jamais modifier un test existant pour le faire passer : s'il semble faux, montrer pourquoi et demander.
5. **Lancer tous les tests** (commande dans `CLAUDE.md`). Tout doit passer. Mettre à jour le `README.md`
   ou le `CLAUDE.md` si l'usage ou une commande change.
6. **Commiter** par petits commits, chacun avec des tests verts : messages en français, au présent, avec
   l'identifiant du ticket.
7. **Relire son propre diff** (`git diff main...HEAD`) en entier : code de débogage, fichier modifié par erreur,
   test existant modifié. Au-delà d'environ 400 lignes, proposer de découper. Puis **faire relire** par le
   sous-agent `relecteur`. Traiter les remarques bloquantes et « à corriger ».
8. **Préparer la description** de la merge request, avec ce plan :

```markdown
## Pourquoi
## Ce qui change
## Critères d'acceptation (critère | fait | test qui le prouve)
## Comment tester
## Résultat des tests
## Relecture (verdict du relecteur et suites données)
## Risques et retour arrière (ce qui pourrait casser ailleurs ; comment annuler)
## Points d'attention
Closes #<numéro du ticket GitLab, s'il existe>
```

9. **Publier**, selon le cas :
   - pas de dépôt GitLab : écrire la description dans `merge-requests/<identifiant>.md` (dossier ignoré par git) ;
   - dépôt GitLab et `glab` connecté : demander l'accord, puis `git push -u origin <branche>` et
     `glab mr create --title "<titre> (<identifiant>)" --description "$(cat <fichier>)" --target-branch main`.
10. **Résumer** : branche, commits, tests, verdict du relecteur, lien ou chemin de la merge request.
    Ne jamais fusionner : la fusion est la décision d'un humain, après un pipeline vert.
