# Analyses e-commerce sur BigQuery

Dépôt des analyses de l'équipe e-commerce. Les données sont dans BigQuery, projet `<projet>`.
Sommaire de la couche sémantique : @semantique/README.md

## Tables principales (noms complets)

| Usage | Table | Partition (filtre obligatoire) |
|---|---|---|
| Lignes de commande (CA, articles) | `<projet>.<dataset>.<table>` | `<colonne date>` |
| Commandes | `<projet>.<dataset>.<table>` | `<colonne date>` |
| Clients | `<projet>.<dataset>.<table>` | - |
| Envois d'e-mails | `<projet>.<dataset>.<table>` | `<colonne date>` |
| Calendrier commercial | `<projet>.<dataset>.<table>` | - |

## Règles

1. Avant toute requête, lire les fiches de `semantique/` des tables et des métriques utilisées, et les citer.
2. Si un terme n'est défini nulle part (par exemple « client actif »), demander au lieu de choisir.
3. N'utiliser que les jointures listées dans les fiches. Toujours filtrer la colonne de partition.
   Jamais de `SELECT *`. `LIMIT` ne réduit pas le coût.
4. D'abord `bq query --use_legacy_sql=false --dry_run '...'` : annoncer le volume lu.
   Au-delà de 5 Go, prévenir et attendre l'accord.
5. Exécuter avec `bq query --use_legacy_sql=false --maximum_bytes_billed=5000000000 '...'`
   (le hook refuse une exécution sans plafond).
6. Lecture seule : aucune requête qui crée, modifie ou supprime une table.
7. Annoncer les contrôles faits : lignes, doublons après jointure (`COUNT(*)` contre `COUNT(DISTINCT ...)`),
   total comparé à une référence connue.
8. Répondre avec : définition utilisée, filtres, requête, résultat, volume lu, limites.
9. Les définitions des métriques vivent dans `semantique/` seulement, pas dans ce fichier.
10. Tutoyer ; expliquer en français simple.
