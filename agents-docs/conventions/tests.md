# Conventions de tests

## Où et comment

- Chaque projet a ses tests dans `projets/<projet>/tests/`, avec pytest.
- Lancer tous les tests d'un projet : `cd projets/<projet> && uv run pytest -q`.
- Dans le kit, un hook relance les tests du projet après chaque modification d'un fichier Python.

## Écrire un test

- Un test par critère d'acceptation du ticket, dans le fichier de tests du sujet
  (`tests/test_delais.py` pour la page des délais).
- Un nom en français qui dit le critère : `test_filtre_famille_ignore_les_majuscules`.
- La valeur attendue vient du ticket ou d'un calcul refait à la main, jamais du résultat affiché par le code.
- Un test prouve un critère s'il échouerait sans la modification.

## Règles

- Tous les tests du projet passent avant chaque envoi de la branche, pas seulement les nouveaux.
- Ne jamais modifier ni supprimer un test existant pour le faire passer. S'il semble faux, s'arrêter,
  montrer le calcul et demander.
- Un critère qui ne se vérifie pas par un test (avis d'un utilisateur) est signalé dans la merge request,
  pour la relecture.
