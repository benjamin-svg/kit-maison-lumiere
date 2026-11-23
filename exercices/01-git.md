# Exercice 01 : Git avec Claude

## Objectif

Voir Git fonctionner dans le kit, en demandant chaque action à Claude, et lire ce qu'il fait.
Vous ne tapez aucune commande : vous écrivez vos demandes en français, et vous lisez les commandes qu'il lance.

Ce que vous allez apprendre :

1. Lire l'état d'un dépôt, et comprendre pourquoi certains fichiers ne sont pas suivis.
2. Faire un commit, et reconnaître les deux étapes : indexer, puis enregistrer.
3. Provoquer un conflit, le lire, et choisir vous-même la version à garder.

## Durée

- **En salle, 15 min** : étapes 1 à 3, puis 5 min de mise en commun.
- **En autonomie, 15 min** : étapes 4 et 5, et « Pour aller plus loin ».

## Les mots de la partie Git

- **Dépôt** : le dossier du projet et son sous-dossier caché `.git`, où Git range les versions.
- **Index** : la liste de ce qui sera ajouté au prochain commit. `git add` y place un fichier.
- **Commit** : une version enregistrée de tous les fichiers suivis, avec l'auteur, la date et un message qui dit pourquoi.
- **Branche** : une suite de commits à part. `main` est la branche de référence, celle qui fonctionne.
- **Fusion** (merge) : réunir les modifications d'une branche dans une autre.
- **Conflit** : la même ligne a changé sur les deux branches. Git ne sait pas laquelle garder et attend une décision.
- **Merge request** (GitLab) : une page qui demande de fusionner une branche dans `main`, montre les
  modifications et reçoit la relecture.

## Étape 1 : l'état du dépôt (3 min)

> « Explique-moi l'état de ce dépôt : la branche, les derniers commits, les fichiers modifiés et ceux que Git ignore. Pourquoi la base DuckDB et les CSV ne sont-ils pas suivis ? »

**À observer** : Claude lance `git status` et `git log`, et lit le fichier `.gitignore`.

**Pourquoi** : un script produit les données. On garde le script dans le dépôt, pas le résultat, qu'on peut
toujours recréer. Les dossiers `travail/<prénom>/` ne sont pas suivis non plus (brouillons personnels),
sauf `travail/<prénom>/git/`, qui sert à cet exercice.

Si Git refuse le premier commit parce qu'il ne connaît pas votre nom :

> « Configure Git pour ce dépôt seulement, avec mon prénom et l'adresse prenom@exemple.fr. »

## Étape 2 : un premier commit (4 min)

> « Crée le fichier travail/<prénom>/git/ordre-du-jour.md avec un titre et cinq points numérotés pour une réunion d'équipe sur les soldes d'été. Puis fais un commit avec un message clair en français. Montre-moi les commandes utilisées. »

**À observer** : deux commandes. `git add` place le fichier dans l'index, c'est-à-dire ce qui sera ajouté au
prochain commit. Puis `git commit -m "..."` enregistre la version.

**Pourquoi** : ce sont les deux étapes d'un commit. On choisit d'abord ce qu'on enregistre, puis on l'enregistre.

## Étape 3 : un conflit (8 min)

Copiez cette demande :

> « Je veux voir un conflit Git. Crée une branche essai/ordre-du-jour. Sur cette branche, remplace le point 3 de travail/<prénom>/git/ordre-du-jour.md par "3. Bilan du Black Friday", puis fais un commit. Reviens sur main, remplace le même point 3 par "3. Préparation des soldes d'hiver", et fais un commit. Enfin, fusionne essai/ordre-du-jour dans main. Arrête-toi au conflit et explique-le-moi sans le résoudre. »

**À observer** :
- `git switch -c essai/ordre-du-jour` crée la branche et s'y place, `git switch main` revient sur main.
- Au moment de `git merge`, Git signale un conflit. Ouvrez le fichier : les marqueurs `<<<<<<<`, `=======`
  et `>>>>>>>` entourent les deux versions du point 3.

Puis décidez vous-même :

> « Garde les deux points : "3. Bilan du Black Friday" puis "4. Préparation des soldes d'hiver", renumérote la suite, termine la fusion et montre-moi le résultat. »

**À observer** : Claude retire les marqueurs, puis lance `git add` et `git commit` pour terminer la fusion.

**Pourquoi** : Git ne choisit pas. Le bon choix dépend du contenu : vous décidez, Claude exécute.

## Étape 4 : l'historique (5 min, en autonomie)

> « Montre-moi l'historique sous forme de graphe, avec toutes les branches, et explique chaque ligne. »

**À observer** : `git log --oneline --graph --all`. Le commit de fusion a deux parents : le dernier commit de
main et le dernier commit de la branche.

## Étape 5 : et sur GitLab ? (10 min, en autonomie)

> « Si ce dépôt était sur le GitLab de l'entreprise, explique-moi, étape par étape et sans rien exécuter, ce qui se passerait entre la création de ma branche et la fusion dans main : git push, merge request, relecture, vérifications automatiques, fusion. Qu'est-ce qui change par rapport à ce que nous venons de faire ? »

**À observer** : ici, vous avez fusionné seul. Sur GitLab, la fusion passe par une merge request : une page qui
montre les modifications, relance les vérifications automatiques, reçoit la relecture d'un collègue et garde
une trace de la décision. L'exercice 02 refait ce cycle avec un dépôt distant qui joue le rôle de GitLab.

## Comment vérifier

- `git log --oneline --graph --all` montre la branche `essai/ordre-du-jour` et un commit de fusion.
- `travail/<prénom>/git/ordre-du-jour.md` ne contient plus aucun marqueur de conflit.
- `git status` n'affiche aucune modification en attente.

## Pour aller plus loin

- Demandez à Claude d'annuler le commit de fusion avec `git revert`, puis expliquez pourquoi l'historique
  garde les deux commits.
- Demandez-lui de créer un deuxième dossier de travail sur une autre branche, avec `git worktree add`, et
  d'expliquer à quoi cela sert quand deux sessions de Claude travaillent en même temps.
