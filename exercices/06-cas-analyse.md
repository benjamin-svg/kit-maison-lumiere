# Exercice 06 - Un cas d'analyse complet, de la question du marketing à la note

## Objectif

Traiter trois questions que le marketing pose vraiment, en s'appuyant sur la couche sémantique de l'exercice 03 :
choisir les bonnes tables, repérer les pièges, faire vérifier les chiffres, et rendre une note d'une page
qu'un non-spécialiste comprend. Puis préparer le passage aux vraies données : réécrire une requête pour BigQuery.

Prérequis : l'exercice 03 (fiches `commandes_jour` et `clients`, métriques `client_actif` et `panier_moyen_ht`).

## Durée

1 h 20 (parcours de Céline) : étapes 1, 2 et 4 (1 h 05), puis 15 min de bilan. Les étapes 3 et 5 se font en autonomie.

## Étape 1 - Le bilan d'une opération (20 min)

> « /analyse Fais le bilan des soldes d'été 2025 comparés à ceux de 2024 : chiffre d'affaires net HT, nombre de commandes et panier moyen, par canal et au total. Puis donne les familles de produits qui progressent le plus et celles qui reculent. Prends les dates dans le calendrier commercial. »

**À observer** :
- Les dates des soldes changent d'une année à l'autre : Claude les lit dans `calendrier_commercial`, il ne les devine pas.
  Les deux périodes ont-elles le même nombre de jours ?
- La marketplace n'existait pas avant mars 2024 : sa progression est forte, mais que vaut-elle ?
- Une famille recule nettement : laquelle, et qu'en dire sans aller trop loin ?
- Contrôles : la somme des canaux égale le total ; le total est recoupé avec `commandes_jour` (et l'écart, expliqué).

## Étape 2 - L'e-mail a-t-il fait acheter ? (30 min)

Le marketing demande : « Notre e-mail de la vente privée d'octobre 2025 a-t-il fait acheter ? »

> « /analyse Pour la vente privée web d'octobre 2025, l'e-mail envoyé juste avant a-t-il fait acheter ? Dis-moi d'abord quelles données permettent d'y répondre et lesquelles manquent. »

**À observer** :
- Aucune campagne n'est reliée à une opération dans la base : Claude doit le dire, et proposer une hypothèse
  (la campagne envoyée la veille) au lieu de l'affirmer.
- La comparaison « ouvreurs contre non-ouvreurs » est piégée : ceux qui ouvrent les e-mails sont des clients
  déjà plus actifs, qui achètent plus même sans e-mail. Demandez-le :

> « Les ouvreurs n'achetaient-ils pas déjà plus avant ? Compare avec une semaine normale, deux semaines plus tôt. Et compare plutôt les clients qui ont reçu l'e-mail à ceux, inscrits aussi, qui ne l'ont pas reçu. »

- Chaque semaine, une partie seulement des inscrits reçoit la campagne. Si ce choix est fait au hasard, on a
  un groupe témoin tout trouvé : la comparaison « reçu contre pas reçu » mesure l'effet de l'e-mail.
- Demandez au sous-agent `verificateur` de recalculer les taux d'achat des deux groupes.

## Étape 3 - Les clients actifs touchés par nos e-mails (15 min, en autonomie)

> « /analyse Parmi les clients actifs au 31 décembre 2025, selon notre définition, combien ont reçu au moins une campagne en 2025, combien en ont ouvert au moins une, et combien ont cliqué ? Donne aussi la part de ces clients parmi les actifs. »

**À observer** : la table `emails` ne contient que les envois aux clients inscrits : un client actif non inscrit
n'apparaît pas. Le dénominateur (les actifs, ou les inscrits ?) change la lecture. Claude doit le dire.
Rappel utile pour lundi : sur les vraies données, une « ouverture » est mal mesurée (certaines messageries
ouvrent les e-mails automatiquement) ; le clic est plus fiable.

## Étape 4 - La note pour le marketing (15 min)

> « Écris dans travail/<prénom>/note-marketing.md une note d'une page pour la responsable marketing, à partir de trois analyses de ce dossier : le bilan des soldes d'été 2025, l'effet de l'e-mail de la vente privée d'octobre 2025, et les clients actifs touchés par nos e-mails. Trois messages clés, un tableau par question, les limites, et ce qu'il faudrait pour mieux répondre la prochaine fois. Pas de jargon : chaque mot technique est expliqué ou remplacé. »

Puis :

> « Demande au sous-agent relecteur de relire cette note comme le ferait la responsable marketing : un chiffre est-il faux, ambigu ou sans source ? »

## Étape 5 - Préparer lundi : la même requête sur BigQuery (15 min, en autonomie)

Lisez `lundi/bigquery.md` (coût, `--dry_run`, plafond, syntaxe). Puis :

> « Lis lundi/bigquery.md. Réécris en SQL BigQuery la requête de mon bilan des soldes d'été 2025 (dans travail/<prénom>/analyses/), avec des noms de tables complets de la forme `projet.dataset.table` (invente-les, en le disant), et liste chaque différence de syntaxe avec la version DuckDB. Dis-moi aussi quelle commande bq je lancerais d'abord pour connaître le coût, sans rien exécuter. »

**À observer** : `COUNT(*) FILTER (WHERE ...)` devient `COUNTIF(...)`, les intervalles de dates s'écrivent
autrement, et l'on commence toujours par un `--dry_run`. Comparez avec `modeles/bigquery/CLAUDE.modele.md` et
`modeles/bigquery/claude/skills/analyse-bigquery/SKILL.md` : ce sont les fichiers à copier dans votre dépôt lundi
(le mode d'emploi de la copie est dans `modeles/bigquery/LISEZMOI.md`).

## Bilan (15 min)

Notez dans `travail/<prénom>/bilan.md` : les trois questions que vous poserez lundi sur les vraies données,
les tables dont vous aurez besoin, et ce qu'il faut demander avant (voir `lundi/a-demander.md`).

## Comment vérifier

- Étape 1 : la somme des canaux égale le total ; la marketplace est signalée comme non comparable ;
  le recul d'une famille est chiffré. Ordre de grandeur : environ 330 000 € en 2025, en hausse d'environ 5 %.
- Étape 2 : la note dit clairement qu'aucune campagne n'est reliée à l'opération, que la comparaison
  ouvreurs contre non-ouvreurs est biaisée, et conclut à partir de la comparaison reçu contre pas reçu.
- Étape 3 : le dénominateur est écrit noir sur blanc ; un peu plus de 5 000 clients actifs ont reçu au moins un e-mail.
- Le vérificateur a confirmé au moins un chiffre ; le relecteur n'a plus de remarque bloquante sur la note.
- La requête BigQuery n'a pas été exécutée (il n'y a pas de BigQuery dans le kit) et chaque différence de syntaxe est listée.

## Pour aller plus loin

- Ajoutez à `semantique/` une fiche `emails` avec `/documenter-table emails`, dont le piège « la table ne
  contient que les inscrits ».
- Proposez une table qui relierait chaque campagne à une opération (colonnes, granularité, qui la remplit) :
  c'est la demande à faire à l'équipe CRM pour répondre à la question 2 sur les vraies données.
