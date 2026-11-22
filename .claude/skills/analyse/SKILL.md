---
name: analyse
description: Répond à une question métier chiffrée sur la base DuckDB de formation, selon les pratiques d'un analyste - cadrer la décision, définir l'indicateur avec semantique/, comparer à périmètre égal, contrôler, distinguer constat et cause, rédiger la réponse d'abord, enregistrer dans travail/<prénom>/analyses/. À utiliser pour toute question d'analyse sur les ventes, commandes, clients ou e-mails.
argument-hint: "[question métier]"
---

# Analyse chiffrée

Question : $ARGUMENTS

Si le prénom de la personne n'est pas connu, le demander (il sert au dossier `travail/<prénom>/`).

Cette skill suit les pratiques courantes d'un analyste : partir de la décision, définir l'indicateur avant
de calculer, comparer ce qui est comparable, contrôler chaque chiffre, ne pas confondre un constat et une
cause, et donner la réponse avant le détail.

## 1. Cadrer la question

- **La décision** : qui demande, pour décider quoi ? Si ce n'est pas dit, le demander en une question.
  Une réponse juste à la mauvaise question ne sert à rien.
- **L'indicateur** : lequel, sur quel périmètre (canal, population), sur quelle période, à quelle date.
- **Les ambiguïtés** (« CA » : HT ou TTC ? retours déduits ? annulées ?) : les trancher **avec les définitions
  de `semantique/metriques.yml`**. Si une ambiguïté n'y est pas tranchée, poser la question avant de continuer.
- **Le type de question** : un constat (« combien ? »), une comparaison (« plus ou moins que ? ») ou un effet
  (« est-ce que X a fait acheter ? »). Une question d'effet demande une comparaison avec un groupe ou une
  période témoin : le dire dès le départ.

## 2. Choisir les tables, et dire pourquoi

Lire `semantique/README.md`, `semantique/metriques.yml` et les fiches utiles de `semantique/tables/`.
Annoncer les tables retenues, la métrique utilisée, et pourquoi. Dire aussi quelles tables ont été écartées
et pourquoi (table agrégée non validée, fiche au statut `BROUILLON` ou `A_COMPLETER`).
Vérifier la période réellement couverte par les données : une période incomplète (mois en cours, données
pas encore chargées) ne se compare pas à une période complète.

## 3. Comparer à périmètre égal

Pour toute comparaison (année précédente, autre opération, autre canal) :
- **même durée** et, si possible, même composition en jours de la semaine ; pour une année sur l'autre,
  décaler de 364 jours (52 semaines) plutôt que de prendre les mêmes dates ;
- **même périmètre** : un canal, un magasin ou une offre qui n'existait pas l'an dernier se signale à part ;
- **décomposer** un écart de chiffre d'affaires en nombre de commandes × panier moyen, et par canal ou
  famille : dire d'où vient l'écart ;
- donner les **effectifs** à côté des pourcentages : un taux calculé sur 40 clients ne pèse pas comme un taux
  calculé sur 4 000.

## 4. Écrire la requête et l'expliquer

Requête SQL lisible (CTE nommées, commentaires courts), sans `SELECT *`. L'expliquer bloc par bloc en
français simple : ce que fait chaque partie, et à quoi sert chaque filtre.
Exécution en lecture seule : `uv run python outils/requete.py -f <fichier.sql>`.

## 5. Contrôler

Faire et **annoncer** au minimum ces contrôles, chacun avec son résultat :
- **nombre de lignes** aux étapes importantes (avant et après filtre, avant et après jointure) ;
- **doublons après jointure** (`COUNT(*)` contre `COUNT(DISTINCT clé)`) ;
- **total recoupé** par un autre chemin (autre table, somme des sous-totaux) et écart expliqué ;
- **valeurs vides** dans les colonnes clés ; **valeurs extrêmes** qui pèsent sur une moyenne ;
- **ordre de grandeur** : le résultat est-il plausible face à un chiffre connu (mois précédent, chiffre publié) ?

Si un contrôle échoue, le dire, corriger et recommencer. Proposer le sous-agent `verificateur` pour un recalcul
indépendant (lui donner la question et le chiffre, pas la requête) avant toute diffusion.

## 6. Distinguer le constat et la cause

- Un écart entre deux groupes n'est pas un effet : les clients qui ouvrent un e-mail achetaient déjà plus
  avant. Comparer à un témoin (clients non touchés, période sans l'opération) et dire ce que la comparaison
  ne règle pas.
- Un petit écart sur de petits effectifs peut venir du hasard : le dire, et donner l'ordre de grandeur de
  cette variation quand c'est possible (par exemple l'écart entre deux semaines ordinaires).
- Écrire « les données montrent » pour un constat, « cela suggère » pour une interprétation.

## 7. Rédiger et enregistrer

La réponse commence par **la phrase qui répond à la question**, avec le chiffre arrondi et son unité.
Ensuite : deux ou trois éléments qui l'expliquent, puis les limites. Pas plus de chiffres que nécessaire.

Dans `travail/<prénom>/analyses/AAAA-MM-JJ-<sujet-court>/` :
- `requete.sql` : la requête finale commentée ;
- `resultat.csv` : le résultat (option `--csv` de `outils/requete.py`) ;
- `NOTE.md` : la question et la décision qu'elle sert ; la réponse en une phrase ; les définitions utilisées
  (métrique, période, filtres) ; les contrôles et leurs résultats ; les limites ; la date des données.
  Quelqu'un doit pouvoir refaire le calcul à partir de cette note seule.

## Règles

- Ne jamais modifier `donnees/brutes/` ni la base.
- Chaque chiffre de la réponse vient d'une requête exécutée dans cette session : pas de chiffre de tête.
- Une analyse par dossier, nommé par son sujet : la personne doit pouvoir dire « mon bilan des soldes » et le retrouver.
- Ne pas lire `exercices/` ni `donnees/generer_donnees.py` : calculer à partir des données.
