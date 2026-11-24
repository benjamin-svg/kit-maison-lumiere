# Démonstration 4 : la couche sémantique (10 min)

Ce qu'on voit : Claude écrit le SQL à partir d'une question en français. Avec les définitions du dossier
`semantique/`, il prend la bonne table et le bon calcul. Sans elles, il donne un chiffre plausible et faux.
Et quand une définition manque, il s'arrête et vous la demande.

La base : `donnees/ecommerce.duckdb`, 9 tables. Le dossier `semantique/` décrit ces tables (`tables/`) et
les indicateurs (`metriques.yml`).

## 1. Une question simple

> « Combien de clients ont la carte de fidélité, par région ? Montre la requête SQL et explique-la ligne par ligne. »

À voir : il lit la fiche de la table `clients`, écrit la requête, la lance avec `outils/requete.py`, et annonce
ses contrôles (nombre de lignes, valeurs vides, total).

## 2. La même question, d'abord sans les définitions, puis avec

Tapez `/clear`, puis :

> « Pour cette question uniquement, ne lis pas le dossier semantique/ ni aucun fichier .md du dépôt : regarde seulement la liste des tables avec outils/requete.py --tables, puis réponds vite. Quel est le chiffre d'affaires du canal web en novembre 2025 ? Donne le chiffre et la requête. »

Notez le chiffre. Puis `/clear`, et :

> « /analyse Quel est le chiffre d'affaires du canal web en novembre 2025 ? »

À voir : sans les définitions, il prend souvent `commandes_jour` ou `commandes.montant_ttc`. Avec, il suit la
définition `ca_net_ht` : 360 983 €. Demandez : « Explique l'écart entre les deux chiffres. »

## 3. Un indicateur qui n'est pas défini

> « Quel est le panier moyen HT des commandes web en 2025 ? »

À voir : il trouve `panier_moyen_ht` au statut `A_COMPLETER` dans `metriques.yml`, s'arrête et vous demande
comment le calculer, au lieu d'inventer. Répondez comme le contrôle de gestion : « CA net HT divisé par le
nombre de commandes non annulées. »

## Pour aller plus loin

La version longue de cette démonstration : [l'exercice 03](../exercices/03-couche-semantique.md) (1 h) : écrire deux fiches de tables et trois indicateurs, puis [l'exercice 06](../exercices/06-cas-analyse.md), un cas d'analyse complet.

## Dans votre cas

| Qui | Cas | Ce qu'il faut décrire pour Claude |
|---|---|---|
| Céline | Analyses BigQuery | les 5 tables que vous utilisez le plus, et les indicateurs de vos tableaux de bord |
| Augustin | Churn | la définition du client perdu : fenêtre d'observation, fenêtre de cible, date de référence |
| Olivier | Prévision des commandes web | ce que compte « une commande web » (annulées ? marketplace ?), la table quotidienne utilisée |
| Olivier | Traduction | le glossaire : un seul mot par matière, coupe et gamme, dans chaque langue |
| Maxime | Délais ORLI | les colonnes de l'Excel : unité du délai, format des dates, référence produit |
| Maxime | Portail intranet | les indicateurs affichés dans le portail, pris dans la même couche que les analyses |
