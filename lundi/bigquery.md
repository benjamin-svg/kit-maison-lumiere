# Lundi sur BigQuery : refaire les analyses du kit sur les vraies données

Le kit tourne sur DuckDB, une base locale gratuite. Lundi, les données sont dans BigQuery : la méthode est
la même (couche sémantique, `/analyse`, vérificateur), mais trois choses changent : **le coût**, **la syntaxe**
et **l'outil** qui lance les requêtes.

## 1. Ce qui change

| Dans le kit | Lundi |
|---|---|
| `donnees/ecommerce.duckdb`, sur le poste | BigQuery, dans le projet Google Cloud de l'entreprise |
| `uv run python outils/requete.py "SELECT ..."` | `bq query --use_legacy_sql=false '...'` (ou un serveur MCP) |
| Gratuit, aussi souvent qu'on veut | **Facturé au volume de données lues** |
| `SELECT * FROM commandes` | `` SELECT ... FROM `projet.dataset.commandes` WHERE <filtre de date> `` |
| Le vérificateur relit les CSV de `donnees/brutes/` | Le vérificateur fait une seconde requête : un second coût |
| `semantique/` décrit des tables inventées | `semantique/` décrit vos vraies tables : à écrire avec le métier |

## 2. Le coût

- BigQuery facture le **volume lu** par la requête, pas le nombre de lignes du résultat. Au tarif public
  « à la demande », environ 6,25 $ par téraoctet lu (à vérifier : l'entreprise peut avoir un forfait).
- **`LIMIT` ne réduit pas le coût** : BigQuery lit quand même les colonnes demandées.
- Lire moins : **filtrer la colonne de partition** (souvent la date), ne demander **que les colonnes utiles**
  (jamais `SELECT *`).
- **Estimer avant d'exécuter** : `--dry_run` vérifie la requête et donne le volume qu'elle lirait, sans rien
  lancer ni facturer.

```bash
bq query --use_legacy_sql=false --dry_run 'SELECT ...'
# « Query successfully validated. Assuming the tables are not modified, running this query will process 1234567 bytes of data. »
```

- **Plafonner** : `--maximum_bytes_billed` fait échouer la requête, sans la facturer, si elle lirait plus.

```bash
bq query --use_legacy_sql=false --maximum_bytes_billed=5000000000 'SELECT ...'   # 5 Go au plus
```

- Le kit fournit un **hook** qui refuse une requête lancée sans dry run ni plafond, et toute requête qui écrit :
  `modeles/bigquery/claude/hooks/garde_cout_bq.py`.

## 3. La syntaxe : DuckDB (kit) et BigQuery

Les formules de `semantique/metriques.yml` sont écrites en SQL DuckDB. Elles ne tournent pas telles quelles
sur BigQuery. Les différences que vous rencontrerez dans les exercices :

| Besoin | DuckDB (kit) | BigQuery |
|---|---|---|
| Nom de table | `commandes` | `` `projet.dataset.commandes` `` |
| Compter avec une condition | `COUNT(*) FILTER (WHERE statut <> 'ANNULEE')` | `COUNTIF(statut <> 'ANNULEE')` |
| Sommer avec une condition | `SUM(x) FILTER (WHERE ...)` | `SUM(IF(..., x, 0))` |
| Retirer des jours | `d - INTERVAL 365 DAY` | `DATE_SUB(d, INTERVAL 365 DAY)` |
| Écart en jours | `DATE_DIFF('day', debut, fin)` | `DATE_DIFF(fin, debut, DAY)` (ordre inversé) |
| Semaine du lundi | `DATE_TRUNC('week', d)` | `DATE_TRUNC(d, ISOWEEK)` (`WEEK` commence le dimanche) |
| Année de la semaine | `ISOYEAR(d)` | `EXTRACT(ISOYEAR FROM d)` |
| Conversion | `x::INT`, `DOUBLE` | `CAST(x AS INT64)`, `FLOAT64` |
| Division sans erreur | `x / NULLIF(y, 0)` | `SAFE_DIVIDE(x, y)` |
| Paramètre | `:date_obs` (dans le kit) | `@date_obs`, avec `--parameter=date_obs:DATE:2025-12-31` |
| Date d'un horodatage | `CAST(ts AS DATE)` | `DATE(ts, 'Europe/Paris')` (sinon, jour en heure UTC) |
| `QUALIFY` | toujours permis | permis, mais BigQuery peut exiger un `WHERE` dans la requête : ajouter `WHERE TRUE` |
| Recherche sans majuscules | `ILIKE` | `LOWER(x) LIKE` |

Demandez à Claude : « Traduis cette requête DuckDB en SQL BigQuery et liste chaque différence. »
Puis vérifiez avec un `--dry_run` : il signale les erreurs de syntaxe sans rien coûter.

## 4. L'outil

- **`bq`**, l'outil en ligne de commande de Google Cloud (installé avec le Google Cloud CLI). Connexion :
  `gcloud auth login`. C'est l'option conseillée pour commencer : dry run et plafond sont visibles dans chaque commande.
- **Un serveur MCP BigQuery** (serveur géré par Google, ou MCP Toolbox for Databases) : Claude appelle des outils
  au lieu de taper des commandes. Utile ensuite, pour des requêtes validées transformées en outils
  (« CA net HT entre deux dates »), que Claude appelle sans pouvoir changer la formule.
- **Droits à demander** : lecture seule. En général les rôles `BigQuery Data Viewer` sur les datasets utiles et
  `BigQuery Job User` sur le projet (pour lancer des requêtes). Rien en écriture.

## 5. Mettre en place, lundi matin

À faire à deux la première fois (avec Maxime ou le formateur) : une heure suffit.

1. Créer (ou ouvrir) le dépôt GitLab des analyses, le cloner sur le poste, puis copier les fichiers, depuis le
   dossier du dépôt (remplacez `<kit>` par le chemin du kit) :

   ```bash
   mkdir -p .claude semantique/tables
   cp <kit>/modeles/bigquery/CLAUDE.modele.md CLAUDE.md
   cp -r <kit>/modeles/bigquery/claude/. .claude/
   cp -r <kit>/.claude/skills/documenter-table .claude/skills/
   cp <kit>/semantique/README.md semantique/
   python3 <kit>/modeles/bigquery/tester_garde_cout.py     # « Tous les cas sont conformes. »
   ```

2. Lancer `claude` dans le dépôt, accepter la confiance au dossier, puis demander :
   « Remplis le tableau des tables de CLAUDE.md avec ces noms complets : <liste reçue>. Puis adapte la skill
   documenter-table à BigQuery : le schéma vient de INFORMATION_SCHEMA.COLUMNS, chaque requête passe d'abord
   en --dry_run, et rien n'est exécuté sans plafond. Montre-moi les changements avant de les écrire. »
   (`INFORMATION_SCHEMA` : les tables où BigQuery décrit lui-même les colonnes de chaque table.)
3. Faire ensemble un premier `--dry_run`, puis la même requête avec plafond, sur une petite question.
4. Écrire les fiches des 3 à 5 tables les plus utiles, avec `/documenter-table` adapté à BigQuery :
   le schéma vient de `INFORMATION_SCHEMA.COLUMNS`, la granularité et les pièges viennent du métier.
5. Recopier les métriques validées (CA net HT, nombre de commandes) avec leur formule en SQL BigQuery,
   et les faire valider par leur propriétaire.
6. Poser une question dont vous connaissez la réponse (un chiffre déjà publié) : si Claude ne la retrouve pas,
   la couche sémantique a un trou.

## 6. Ce qu'il faut demander avant

Voir `lundi/a-demander.md` : noms complets des tables, propriétaire des métriques, droits, forfait BigQuery.
