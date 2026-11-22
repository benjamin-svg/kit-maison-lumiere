# Exercice 03 - La couche sémantique

## Objectif

Constater, chiffres à l'appui, ce que change une couche sémantique : la même question posée sans puis avec
`semantique/` ne donne pas le même chiffre. Puis enrichir cette couche (deux fiches de tables, trois métriques)
et s'en servir pour répondre à trois questions métier avec la skill `/analyse`.

## Durée

- Parcours de Céline : 1 heure (étapes 1 à 3, puis la première question de l'étape 4 ; les deux autres en autonomie).
- Parcours d'Olivier et d'Augustin : en autonomie seulement (en salle, ils passent à la méthode ML).

## Rappel

La **couche sémantique** dit ce que veulent dire les données : le rôle de chaque table, sa granularité
(ce que représente une ligne), ses jointures, ses pièges, et la définition unique de chaque indicateur.
Ici, c'est un dossier de fichiers texte (`semantique/`), relu et versionné comme du code.

## Étape 1 - La même question, sans puis avec la couche sémantique (15 min)

Vérifiez d'abord que votre `CLAUDE.md` ne contient pas la définition du chiffre d'affaires (si vous avez
accepté une proposition de `/init` à l'exercice 00) :

> « Est-ce que CLAUDE.md contient une définition du chiffre d'affaires ou d'une métrique ? Réponds oui ou non, sans rien modifier. »

Si oui, remettez la version du kit le temps de l'étape : « Mets de côté mes modifications de CLAUDE.md avec
git stash » (et `git stash pop` à la fin de l'étape). Sinon, Claude recevrait la bonne définition au démarrage,
et la démonstration ne montrerait rien.

Ouvrez une nouvelle session (`/clear`) et donnez **exactement** cette consigne :

> « Pour cette question uniquement, ne lis pas le dossier semantique/ ni aucun fichier .md du dépôt : regarde seulement la liste des tables de la base avec outils/requete.py --tables, puis réponds vite. Quel est le chiffre d'affaires du canal web en novembre 2025 ? Donne le chiffre et la requête. »

Notez le chiffre et la table utilisée. Puis `/clear` à nouveau, et :

> « /analyse Quel est le chiffre d'affaires du canal web en novembre 2025 ? »

**À observer** :
- Sans couche sémantique, Claude prend souvent la table qui paraît la plus simple (`commandes_jour`) ou la colonne
  la plus parlante (`commandes.montant_ttc`). Le chiffre est plausible, mais ce n'est pas le bon.
- Avec `/analyse`, Claude lit `metriques.yml` : CA **net HT**, remises et retours déduits, **commandes annulées
  exclues**, à partir de `lignes_commande`.
- Demandez ensuite : « Explique l'écart entre les deux chiffres, en euros, poste par poste. »
- Si Claude est tombé juste dès la première fois (en ne gardant que les commandes `LIVREE`), demandez-lui :
  « Que donnerait ta première requête en décembre 2025, où des commandes sont encore EN_COURS ? » Il est tombé
  juste par chance : en novembre, il n'y a pas de commande en cours. La couche sémantique évite de compter
  sur la chance.

## Étape 2 - Compléter deux fiches de tables (20 min)

> « /documenter-table commandes_jour »

Validez ou corrigez la fiche proposée, puis :

> « /documenter-table clients »

**À observer** :
- Claude teste la granularité (une ligne par jour et par canal ? par client ?), mesure les valeurs vides,
  vérifie les jointures.
- Pour `commandes_jour`, il compare le total de `ca_ht` à la métrique `ca_net_ht` : y a-t-il un écart ? D'où vient-il ?
  Ce que vous découvrez doit aller dans la section « Pièges connus ».
- Pour `clients`, que signifient les lignes où presque tout est vide ?
- Claude **demande validation** avant d'écrire la fiche. C'est vous qui validez, comme le ferait le métier.

**Valider sans savoir relire le SQL.** Vous ne relisez pas chaque requête : vous vérifiez ce que le métier sait.
- La phrase de granularité (« une ligne = ... ») est-elle juste, dite avec vos mots ?
- Un chiffre que vous connaissez déjà (un total publié, un ordre de grandeur) est-il retrouvé ?
- Chaque piège est-il expliqué en français, avec sa conséquence sur un chiffre ?
- Ce que Claude n'a pas pu savoir est-il écrit comme une question ouverte, pas comme une certitude ?

Le contrôle des requêtes, lui, est confié à une seconde lecture (le sous-agent `relecteur`, étape 3, puis un
collègue lundi). Une fiche relue et acceptée passe au statut `VALIDEE` ; tant qu'elle ne l'est pas, elle reste
`BROUILLON` et ne sert pas à un chiffre diffusé.

## Étape 3 - Compléter les métriques (20 min)

> « Dans semantique/metriques.yml, les métriques client_actif, client_perdu et panier_moyen_ht sont à compléter. Pour chacune, pose-moi les questions à trancher, propose une définition et une formule SQL cohérentes avec ca_net_ht, nb_commandes et la colonne perdu_6m de clients_churn_snapshot, puis teste chaque formule sur la base avant de l'écrire. »

Pour trancher, jouez le rôle du contrôle de gestion, qui a déjà pris ces décisions :

| Métrique | Décision du contrôle de gestion (fictive) |
|---|---|
| `client_actif` | Un identifiant client non vide, avec au moins une commande non annulée dans les 365 jours qui précèdent la date d'observation (incluse). |
| `client_perdu` | À une date de référence : un client qui a déjà commandé avant cette date, et qui ne passe aucune commande non annulée dans les 6 mois qui suivent (182 jours). Même règle que la colonne `perdu_6m`. |
| `panier_moyen_ht` | `ca_net_ht` divisé par `nb_commandes`, avec les mêmes filtres (retours déduits, annulées exclues). |
| Propriétaire | Contrôle de gestion e-commerce. |

Si Claude vous pose une question que ce tableau ne tranche pas, décidez vous-même et notez votre choix
dans le champ `pieges` de la métrique.

Exigez une `formule_sql` **qu'on peut exécuter telle quelle** (une requête complète, avec ses seuls paramètres
de date : `:date_obs` pour les clients, `:date_debut` et `:date_fin` pour le panier), testée sur la base.
Exigez aussi un `exemple` (le résultat de la formule pour une date donnée : il servira de test) et le champ
`additivite` (peut-on additionner ce chiffre d'un jour à l'autre, d'un canal à l'autre ?).
Passez les métriques au statut `BROUILLON`.

Puis faites relire, avant de valider :

> « Demande au sous-agent relecteur de relire semantique/metriques.yml : qu'il exécute chaque formule et recalcule chaque chiffre cité dans les pièges. »

Corrigez ce qu'il signale, puis passez les métriques au statut `VALIDEE`. Une définition se relit comme du code.

## Étape 4 - Trois questions avec `/analyse` (5 min en salle, puis en autonomie)

Posez les trois questions l'une après l'autre :

> « /analyse Quel est le chiffre d'affaires net HT de chaque canal en 2025, et son évolution par rapport à 2024 ? »

> « /analyse Quel est le panier moyen HT des commandes web pendant le Black Friday 2025, comparé à celui des 28 jours qui précèdent l'opération ? Prends les dates dans le calendrier commercial. »

> « /analyse Combien de clients actifs au 31 décembre 2025, selon notre définition de client actif, et quelle part d'entre eux est inscrite aux e-mails ? »

Pour au moins une des trois, demandez :

> « Demande au sous-agent verificateur de recalculer ce chiffre sans voir ta requête. »

**À observer** : les contrôles annoncés (lignes, doublons après jointure, total comparé à une référence),
le choix des tables justifié, le dossier créé dans `travail/<prénom>/analyses/` pour chaque question.

## Comment vérifier

- Étape 1 : **360 983 €** avec `/analyse`. Sans la couche, vous trouverez autre chose (382 369 €, 410 865 €, 494 959 €...).
- Étape 4, repères pour vérifier seul (le formateur a les chiffres exacts) :
  - question 1 : environ 4,7 millions d'euros en 2025 pour les trois canaux réunis, en hausse de 9 à 10 % ;
    la somme des canaux doit égaler le total ;
  - question 2 : le panier moyen baisse pendant le Black Friday (remises), alors que le nombre de commandes par jour augmente fortement ;
  - question 3 : un peu plus de 8 000 clients actifs, dont environ 6 sur 10 inscrits aux e-mails.
- Le vérificateur confirme au moins un des trois chiffres par un autre chemin.
- `semantique/tables/commandes_jour.md` et `semantique/tables/clients.md` sont remplies, au format du README,
  avec au moins un piège chacune.
- `semantique/metriques.yml` n'a plus de `A COMPLETER`, chaque formule tourne telle quelle, et le relecteur
  ne signale plus d'écart.
- Chaque analyse a son `NOTE.md` avec les contrôles et leurs résultats.

## Pour aller plus loin

- Documentez `clients_churn_snapshot` : à quelle date chaque colonne est-elle connue ? Gardez la réponse
  pour l'exercice 05.
- Faites une branche git `semantique/metriques-clients` et commitez vos fiches et vos métriques.
- Reposez la question de l'étape 1 dans une nouvelle session, sans consigne particulière : Claude lit-il
  maintenant `semantique/` de lui-même (grâce au `CLAUDE.md`) ?
