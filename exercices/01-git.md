# Exercice 01 - Git en local, et ce que ferait GitLab

## Objectif

Comprendre les gestes de base de git en les faisant faire par Claude et en les observant : état du dépôt,
commit, branche, conflit et résolution, historique. Puis relier ces gestes à ce que fait GitLab
(dépôt partagé, merge request, pipeline de tests).

## Durée

- **En salle, 15 min** : étapes 1 à 3 (ce sont les étapes 01 à 03 de la slide), puis l'étape 5 racontée par Claude.
- **En autonomie, 25 min de plus** : étapes 4 et 5 en entier, et « Pour aller plus loin ».

## Vocabulaire

- **Dépôt** : le dossier suivi par git, avec tout son historique (dans `.git/`).
- **Commit** : une photo enregistrée de l'état des fichiers, avec un message qui dit pourquoi.
- **Branche** : une ligne de travail parallèle ; `main` est la branche principale.
- **Fusion (merge)** : ramener le travail d'une branche dans une autre.
- **Conflit** : deux branches ont modifié la même ligne ; git ne sait pas choisir et demande à un humain.
- **Merge request** (GitLab) : la demande, sur le serveur, de fusionner une branche dans `main`, avec relecture
  et tests automatiques.

## Étape 1 - L'état du dépôt (5 min)

> « Explique-moi l'état de ce dépôt git : sur quelle branche je suis, les derniers commits, les fichiers modifiés et ceux que git ignore. Pourquoi la base DuckDB et les CSV ne sont-ils pas suivis ? »

**À observer** : Claude lance `git status`, `git log` et lit `.gitignore`. Les données générées ne sont pas
versionnées : on versionne le script qui les produit, pas le résultat. Les dossiers `travail/<prénom>/` ne
le sont pas non plus (brouillons personnels), sauf `travail/<prénom>/git/`, qui sert à cet exercice.

Si git ne connaît pas encore votre nom :

> « Configure git pour ce dépôt seulement avec mon prénom et l'adresse prenom@exemple.fr. »

## Étape 2 - Un premier commit (5 min)

> « Crée le fichier travail/<prénom>/git/ordre-du-jour.md avec un titre et cinq points numérotés pour une réunion d'équipe sur les soldes d'été. Puis fais un commit avec un message clair en français. Montre-moi la commande utilisée. »

**À observer** : `git add` (choisir ce qui entre dans le commit) puis `git commit -m "..."`.

## Étape 3 - Une branche et un conflit volontaire (15 min)

> « Je veux voir un conflit git. Crée une branche essai/ordre-du-jour, et sur cette branche remplace le point 3 de travail/<prénom>/git/ordre-du-jour.md par "3. Bilan du Black Friday", puis commite. Reviens ensuite sur main, remplace le même point 3 par "3. Préparation des soldes d'hiver", et commite. Enfin, fusionne essai/ordre-du-jour dans main. Arrête-toi au conflit et explique-le-moi sans le résoudre. »

**À observer** :
- `git switch -c` (ou `git checkout -b`) pour créer la branche, `git switch main` pour revenir ;
- au moment de `git merge`, git signale un conflit ; le fichier contient des marqueurs
  `<<<<<<<`, `=======`, `>>>>>>>` qui encadrent les deux versions.

Puis décidez vous-même :

> « Garde les deux points : "3. Bilan du Black Friday" puis "4. Préparation des soldes d'hiver", renumérote la suite, termine la fusion et montre-moi le résultat. »

**À observer** : la résolution est un choix humain ; Claude l'exécute (`git add` puis `git commit`).

## Étape 4 - L'historique (5 min)

> « Montre-moi l'historique sous forme de graphe, avec toutes les branches, et explique chaque ligne. »

**À observer** : `git log --oneline --graph --all` ; le commit de fusion a deux parents.

## Étape 5 - Et sur GitLab ? (10 min)

> « Si ce dépôt était hébergé sur le GitLab de l'entreprise, explique-moi, étape par étape et sans rien exécuter, ce qui se passerait entre la création de ma branche et la fusion dans main : git push, merge request, pipeline de tests, relecture, fusion. Qu'est-ce qui change par rapport à ce que nous venons de faire en local ? »

**À observer** : en local, vous avez fusionné seul(e) ; sur GitLab, la fusion passe par une merge request :
une page qui montre les différences, lance automatiquement les tests (pipeline), recueille la relecture
d'un collègue, et garde une trace de la décision. Les exercices suivants reproduisent cette chaîne en local.

## Comment vérifier

- `git log --oneline --graph --all` montre la branche `essai/ordre-du-jour` et un commit de fusion.
- `travail/<prénom>/git/ordre-du-jour.md` ne contient plus aucun marqueur de conflit.
- `git status` est propre (le dossier `travail/` n'est pas suivi, sauf `travail/<prénom>/git/`, commité).

## Pour aller plus loin

- Demandez à Claude d'annuler le dernier commit **sans perdre les modifications** (`git reset --soft HEAD~1`),
  puis de le refaire, en expliquant la différence avec `git revert`.
- Demandez-lui de créer un « tag » `v1.0-formation` et d'expliquer à quoi servent les tags dans une livraison.
