# Démonstration 2 : Git (8 min)

Ce qu'on voit : un commit en deux temps, une branche, et un conflit que vous tranchez vous-même.
Vous ne tapez aucune commande : vous écrivez en français, et vous lisez les commandes que Claude lance.

Si Git refuse le commit parce qu'il ne connaît pas votre nom :
« Configure Git pour ce dépôt seulement, avec mon prénom et l'adresse prenom@exemple.fr. »

## 1. Un commit

> « Crée le fichier travail/<prénom>/git/soldes.md avec un titre et trois lignes : la date des soldes, la remise maximale, les familles concernées. Puis fais un commit avec un message clair en français. Montre-moi les commandes. »

À voir : `git add` place le fichier dans l'index (ce qui sera enregistré), puis `git commit` enregistre la version.

## 2. Un conflit

> « Crée la branche essai/soldes. Sur cette branche, remplace la ligne de la date par "Soldes à partir du 24 juin", puis fais un commit. Reviens sur main, remplace la même ligne par "Soldes à partir du 1er juillet", puis fais un commit. Enfin, fusionne essai/soldes dans main. Arrête-toi au conflit et explique-le-moi sans le résoudre. »

À voir : `git switch -c` crée la branche. Au moment de `git merge`, Git s'arrête : la même ligne a changé des
deux côtés. Les marqueurs `<<<<<<<`, `=======` et `>>>>>>>` entourent les deux versions.

## 3. Vous décidez

> « Garde la date du 24 juin, termine la fusion, puis montre-moi l'historique sous forme de graphe. »

À voir : le commit de fusion a deux parents. Git ne choisit pas : vous décidez, Claude exécute.

## Pour aller plus loin

La version longue de cette démonstration : [l'exercice 01](../exercices/01-git.md) (15 min) : l'état du dépôt, l'historique, ce qui change sur GitLab.

## Dans votre cas

| Qui | Cas | Ce qui va dans le dépôt Git |
|---|---|---|
| Augustin | Churn | le flux Dataiku exporté, puis le script du modèle et sa fiche de validation |
| Céline | Analyses BigQuery | chaque analyse terminée (question, SQL, résultat, contrôles) et les fiches des tables |
| Olivier | Prévision des commandes web | le script de prévision et le chargement du plan commercial |
| Olivier | Traduction | le script, le guide de ton et le glossaire de chaque langue |
| Maxime | Portail intranet | le code du portail, sur le GitLab de l'entreprise, une branche par demande |
| Maxime | Délais ORLI | le script qui lit l'Excel et prépare les changements |
| Maxime | Visuels produits | le script de traitement des photos (pas les photos elles-mêmes) |
