# Démonstration 1 : Claude Code (8 min)

Ce qu'on voit : Claude connaît le projet grâce à `CLAUDE.md`, prépare un plan sans rien modifier, suit une
procédure écrite (une skill), et un hook bloque une action interdite.

Avant de commencer : tapez `/hooks`. Deux hooks doivent apparaître (`garde_fou.py` et `lancer_tests.py`).
Sinon, appelez le formateur et sautez l'étape 4.

## 1. Ce que Claude sait du projet

> « Je suis <prénom>. Explique-moi ce dossier et tes règles. »

À voir : il répond presque sans ouvrir de fichiers et cite les règles du kit. Il a lu `CLAUDE.md` au démarrage.

## 2. Le mode plan

Appuyez sur Maj+Tab jusqu'à voir « plan mode on », puis :

> « Propose un plan pour ajouter au portail une page des 10 produits les plus vendus du mois. »

À voir : il pose des questions (en quantité ou en chiffre d'affaires ? quel mois ?), écrit un plan, et ne
modifie aucun fichier. Refusez le plan : on ne le réalise pas.

## 3. Une skill

Repassez en mode normal (Maj+Tab), puis :

> « /analyse Combien de commandes web non annulées ont été passées en décembre 2025 ? »

À voir : il suit les étapes écrites dans `.claude/skills/analyse/SKILL.md`, lit `semantique/`, montre sa
requête et ses contrôles. Résultat attendu : 2 573.

## 4. Un hook

> « Crée le dossier vide travail/<prénom>/vide. Puis lance exactement cette commande, je veux voir le garde-fou : rm -rf travail/<prénom>/vide »

À voir : « Refusé par le garde-fou de la formation ». Ce texte vient du hook, pas de Claude : il bloque même
si personne n'a pensé à le demander.

## Pour aller plus loin

La version longue de cette démonstration : [l'exercice 00](../exercices/00-prise-en-main.md) (30 min) : /rewind, un sous-agent, une règle dans CLAUDE.md.

## Dans votre cas

| Qui | Cas | CLAUDE.md | Une skill | Un hook |
|---|---|---|---|---|
| Augustin | Churn | ce que veut dire « client perdu » chez vous, où sont les données | /modeliser, puis un /churn-mensuel | refuser l'écriture dans les tables de production |
| Céline | Analyses BigQuery | les règles de l'équipe, où sont les définitions | /analyse | annoncer le coût d'une requête avant de la lancer |
| Olivier | Prévision des commandes web | les séries suivies, les horizons demandés | /prevision-hebdo | comparer l'erreur au modèle précédent |
| Olivier | Traduction | les langues, où sont le guide de ton et le glossaire | /traduire (guide de ton et glossaire) | refuser l'écriture dans les fichiers sources |
| Maxime | Portail intranet | la pile technique, les commandes pour lancer et tester | /recette, /nouvelle-appli | relancer les tests après chaque modification |
| Maxime | Délais ORLI | les colonnes de l'Excel du lecteur Z | /orli-delais | refuser l'envoi à ORLI sans validation |
| Maxime | Visuels produits | les formats d'image du site | les consignes de prise de vue | refuser l'écrasement des photos d'origine |
