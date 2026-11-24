---
name: test-dev
description: Teste le travail sur un ticket - pour chaque critère d'acceptation, vérifie qu'un test automatisé le prouve et écrit ceux qui manquent, puis lance tous les tests du projet et montre, critère par critère, le test et son résultat. Ne modifie jamais un test existant pour le faire passer. Étape du cycle start-dev, développement, test-dev, sync-dev, verify, ship-dev, close-dev.
argument-hint: "[identifiant du ticket, facultatif]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git status*), Bash(git diff*), Bash(git branch*), Bash(git worktree list*), Bash(git rev-parse*), Bash(uv run *), Bash(cd *)
---

# Tester un ticket

Ticket : $ARGUMENTS (facultatif).

Pourquoi cette skill : un critère du ticket n'est tenu que si un test le prouve, et ce test sera relancé à
chaque modification, puis par la CI de GitLab. Lancer **tous** les tests, pas seulement les nouveaux, montre
aussi ce que la modification a pu casser ailleurs (la page Délais fournisseurs du vendredi).

## Étapes

1. **Lire les conventions de tests** : `agents-docs/conventions/tests.md` (dossier principal du kit). Elles
   priment sur les exemples de cette skill (emplacement, nom des tests). Absentes : suivre cette skill.
2. **Trouver la branche du ticket**, comme dans /sync-dev : `git branch --show-current` doit commencer par
   `ticket/`. Sinon, aller dans `.worktrees/<identifiant>` (depuis le dossier principal du kit). Sinon,
   demander. Travailler dans ce worktree.
3. **Relire le ticket** (`projets/*/tickets/<identifiant>-*.md`) et numéroter ses critères d'acceptation.
   Un critère qui ne se vérifie pas par un test (« un germanophone valide le guide ») : le dire, et le garder
   pour la relecture humaine.
4. **Faire le lien critère → test** : dans `projets/<projet>/tests/`, chercher pour chaque critère le test qui le
   prouve (nom du fichier et nom du test). Un test prouve un critère s'il échouerait sans la modification.
5. **Écrire les tests qui manquent**, un par critère, dans le fichier de tests du sujet
   (`tests/test_delais.py` pour la page des délais). Un nom qui dit le critère, en français
   (`test_filtre_famille_ignore_les_majuscules`). Des valeurs attendues tirées du ticket ou des données, pas
   recopiées du résultat obtenu.
6. **Lancer tous les tests du projet** : `uv run pytest -q` dans `projets/<projet>/`.
   - Un nouveau test échoue : dire si c'est le code qui ne tient pas le critère (à corriger dans le
     développement) ou le test qui se trompe (le montrer, et demander avant de le changer).
   - Un ancien test échoue : la modification a cassé quelque chose. S'arrêter, montrer le test, et **ne jamais
     le modifier pour qu'il passe** sans l'accord de la personne.
7. **Ne pas commiter** : /sync-dev enregistre et envoie les tests avec le reste du travail, et reprend ce
   tableau dans la merge request.

## Ce que tu affiches à la fin

```
Tests du ticket <identifiant>
| Critère | Test qui le prouve | Résultat |
| 1. … | tests/test_delais.py::test_… | réussi |
| 4. … | (relecture humaine) | à vérifier |
✓ Tests ajoutés : <n>
✓ Tous les tests du projet : <résultat de pytest>
```

Puis la suite : « Lance /sync-dev pour enregistrer et envoyer ce travail (la merge request se met à jour),
puis /verify pour voir l'application tourner. »
