---
name: recette
description: Transforme un retour de recette (anomalie signalée par un utilisateur) en test qui échoue, cherche la cause plutôt que le symptôme, corrige sans casser les autres tests, vérifie les autres endroits et les résultats déjà diffusés, puis résume pour la personne qui a signalé l'anomalie. À utiliser quand un ticket de recette ou un bug est signalé sur le projet.
argument-hint: "[fichier du ticket de recette]"
---

# De la recette au test, puis à la correction

Retour de recette : $ARGUMENTS (un fichier de `tickets/`, ou un numéro de ticket GitLab : `glab issue view <n>`).

Cette skill suit les pratiques courantes de correction d'anomalie : reproduire avant de corriger, garder
la preuve dans un test de non-régression, corriger la cause et non le symptôme, chercher le même défaut
ailleurs, et faire confirmer la correction par la personne qui l'a signalée.

## Étapes

1. **Lire** le ticket et le `CLAUDE.md` du projet. Reformuler l'anomalie : ce qui est constaté, ce qui est
   attendu, et comment le reproduire. Si le résultat attendu n'est pas clair, le faire préciser.
2. **Reproduire** à la main (petit script ou appel de l'API avec le client de test) et montrer le résultat faux.
3. **Écrire un test qui échoue** dans `tests/` du projet : le plus petit test qui montre l'anomalie, au plus
   près de la règle fautive, avec un nom qui décrit le comportement attendu. Lancer les tests (commande dans `CLAUDE.md`) :
   **montrer que ce test échoue**, et pour la bonne raison. (Le hook relance les tests après chaque
   modification et signalera l'échec : c'est attendu.)
4. **Trouver la cause** : expliquer en deux ou trois phrases simples pourquoi le code se trompe. Remonter
   jusqu'à la vraie cause (« pourquoi ? » plusieurs fois) : trier des nombres lus comme du texte est la cause,
   pas l'ordre affiché.
5. **Corriger** la cause, au plus simple, sans changement hors du ticket. Ne jamais modifier un test existant
   pour le faire passer. Si un test existant contredit le ticket (il attend l'ancien comportement), s'arrêter :
   montrer le calcul qui prouve que le test est faux, et demander l'autorisation de le corriger. Le dire aussi
   dans le résumé.
6. **Relancer tous les tests** jusqu'à ce qu'ils passent tous. Montrer que le nouveau test échoue sans la
   correction (`git stash` avant le commit, ou `git restore --source=main <fichier>` après).
7. **Chercher le même défaut ailleurs** (même fonction appelée ailleurs, même façon de lire une colonne) et
   **les résultats déjà diffusés** que l'anomalie a pu fausser (une page consultée, un export envoyé) : qui
   faut-il prévenir ?
8. **Résumer** pour la personne qui a signalé l'anomalie :
   - la cause, en une phrase ;
   - le test ajouté et ce qu'il vérifie ;
   - la correction (fichier, lignes) ;
   - le résultat des tests avant et après ;
   - les autres endroits à risque et les résultats à revoir ;
   - ce qu'elle doit vérifier elle-même pour clore la recette.

Si on est sur une branche git dédiée, proposer un commit : « Corrige <anomalie> (T-xxx) ».
