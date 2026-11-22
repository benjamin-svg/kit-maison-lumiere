---
name: analyse-bigquery
description: Répondre à une question chiffrée (ventes, clients, e-mails, opérations) à partir de BigQuery, selon les pratiques d'un analyste - cadrer la décision, définir l'indicateur avec la couche sémantique, comparer à périmètre égal, estimer le coût avant d'exécuter, contrôler, distinguer constat et cause. À utiliser pour toute analyse sur les vraies données.
argument-hint: "[question métier]"
---

# Analyse sur BigQuery

Question : $ARGUMENTS

1. **Cadrer** : qui demande, pour décider quoi ? Quel indicateur, quel périmètre, quelle période ?
   Constat, comparaison ou effet ? (un effet demande un groupe ou une période témoin). Si un mot est ambigu, demander.
2. **Lire** `semantique/README.md`, puis les fiches des tables et des métriques concernées. Citer les fiches lues.
   Définition manquante, en double ou au statut `BROUILLON` : s'arrêter et demander.
   Vérifier la fraîcheur : jusqu'à quelle date les données sont-elles chargées ?
3. **Comparer à périmètre égal** : même durée, décalage de 364 jours d'une année sur l'autre, même périmètre
   (un canal nouveau se signale à part), écart décomposé en commandes × panier, effectifs à côté des taux.
4. **Partir d'une requête validée** proche, si la fiche en donne une.
5. **Écrire la requête** en SQL BigQuery standard : noms complets `` `projet.dataset.table` ``, filtre sur la
   partition, jointures des fiches, pas de `SELECT *`, dates en heure de Paris (`DATE(ts, 'Europe/Paris')`).
   L'expliquer en quelques phrases.
6. **Estimer le coût** : `bq query --use_legacy_sql=false --dry_run '<requête>'`. Annoncer le volume lu en Go.
   Au-delà de 5 Go : proposer de réduire (période, colonnes) et attendre l'accord.
7. **Exécuter** avec `--maximum_bytes_billed=5000000000` et `--format=csv` si le résultat est un tableau.
8. **Contrôler** : nombre de lignes ; `COUNT(*)` contre `COUNT(DISTINCT clé)` après chaque jointure ;
   valeurs vides et extrêmes ; somme des parties égale au total ; ordre de grandeur comparé à un chiffre connu.
9. **Distinguer constat et cause** : un écart entre clients touchés et non touchés n'est pas un effet sans
   témoin comparable ; un petit écart sur de petits effectifs peut venir du hasard.
10. **Enregistrer** dans `analyses/<AAAA-MM-JJ>-<sujet>/` : `requete.sql`, `resultat.csv`, `NOTE.md`
    (question et décision, définitions, filtres, résultat, contrôles, volume lu, date des données, limites).
11. **Restituer** : la phrase qui répond d'abord, avec le chiffre arrondi et son unité ; puis ce qui
    l'explique ; puis les limites.

## Pour vérifier un chiffre

Le sous-agent de vérification fait une seconde requête, par un autre chemin : c'est un second coût.
Lui demander aussi un dry run d'abord.
