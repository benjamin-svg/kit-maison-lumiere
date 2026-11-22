# Lundi sur BigQuery : prévision et churn

Exemples à adapter, pour Olivier (prévision) et Augustin (churn). Les noms de tables sont **inventés**
(`projet.ventes.commandes`, etc.) : remplacez-les par les vrais, et faites d'abord un `--dry_run` (voir `bigquery.md`).
Ces requêtes n'ont pas été exécutées sur un vrai BigQuery : demandez à Claude de les relire avec vous, puis
vérifiez-les par un dry run.

## 1. Prévision des commandes web

### La série hebdomadaire, en semaines ISO

```sql
-- Commandes web non annulées par semaine (du lundi au dimanche), semaines complètes seulement.
SELECT
  DATE_TRUNC(date_commande, ISOWEEK) AS semaine,
  EXTRACT(ISOYEAR FROM date_commande) AS annee_iso,
  EXTRACT(ISOWEEK FROM date_commande) AS num_semaine,
  COUNT(DISTINCT id_commande) AS nb_commandes
FROM `projet.ventes.commandes`
WHERE canal = 'WEB'
  AND statut <> 'ANNULEE'
  AND date_commande BETWEEN DATE '2023-01-02' AND DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Paris'), ISOWEEK), INTERVAL 1 DAY)
GROUP BY semaine, annee_iso, num_semaine
ORDER BY semaine;
```

La semaine 53 (2026 en a une, du 28/12/2026 au 03/01/2027) : pour « même semaine l'an dernier », prendre la
semaine 364 jours avant (`DATE_SUB(semaine, INTERVAL 364 DAY)`), pas le même numéro.

### Une méthode concurrente : ARIMA_PLUS_XREG, avec le plan commercial

```sql
CREATE OR REPLACE MODEL `projet.prevision.m_xreg`
OPTIONS (
  model_type = 'ARIMA_PLUS_XREG',
  time_series_timestamp_col = 'semaine',
  time_series_data_col = 'nb_commandes'
) AS
SELECT semaine, nb_commandes, soldes, vente_privee, black_friday   -- 0 ou 1 par semaine, d'après le plan
FROM `projet.prevision.serie_web_avec_plan`
WHERE semaine < DATE '2025-06-30';      -- apprentissage : seulement le passé de la date d'origine

-- Prévision à 12 semaines, avec le plan des semaines à venir DANS SA VERSION CONNUE à la date d'origine
SELECT *
FROM ML.FORECAST(
  MODEL `projet.prevision.m_xreg`,
  STRUCT(12 AS horizon, 0.8 AS confidence_level),
  (SELECT semaine, soldes, vente_privee, black_friday
   FROM `projet.prevision.plan_version_du_jour`));
```

La table `plan_version_du_jour` est la clé : pour une date d'origine, elle garde, pour chaque opération, la
dernière version **publiée avant** cette date. On la recalcule à chaque date d'origine du backtest :

```sql
-- plan_version_du_jour.sql, lancé avec --parameter=date_origine:DATE:2025-06-30
WITH versions_connues AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY id_operation ORDER BY version DESC) AS rang
  FROM `projet.marketing.plan_commercial`
  WHERE date_version < @date_origine               -- publiée avant le jour de la prévision
),
plan AS (SELECT * FROM versions_connues WHERE rang = 1 AND canaux IN ('TOUS', 'WEB')),
semaines AS (
  SELECT semaine
  FROM UNNEST(GENERATE_DATE_ARRAY(DATE_TRUNC(@date_origine, ISOWEEK),
                                  DATE_ADD(DATE_TRUNC(@date_origine, ISOWEEK), INTERVAL 11 WEEK),
                                  INTERVAL 1 WEEK)) AS semaine
)
SELECT s.semaine,
       MAX(IF(p.type_operation = 'SOLDES', 1, 0))       AS soldes,
       MAX(IF(p.type_operation = 'VENTE_PRIVEE', 1, 0)) AS vente_privee,
       MAX(IF(p.type_operation = 'BLACK_FRIDAY', 1, 0)) AS black_friday
FROM semaines s
LEFT JOIN plan p
  ON p.date_debut <= DATE_ADD(s.semaine, INTERVAL 6 DAY) AND p.date_fin >= s.semaine   -- l'opération touche la semaine
GROUP BY s.semaine
ORDER BY s.semaine;
```

Contrôle : pour une opération déplacée (dans le kit, la vente privée de septembre 2025), la version 1 doit
sortir pour une origine antérieure au déplacement, la version 2 ensuite. La même requête, avec
`date_origine` remplacée par chaque semaine passée, construit `serie_web_avec_plan` pour l'apprentissage.

Créer un modèle écrit dans un dataset : il faut un dataset de travail où vous avez le droit d'écrire
(le hook de coût du kit refuse `CREATE` : l'adapter pour ce seul dataset).

Comparer cette méthode à la règle simple **sur le même backtest** (mêmes semaines, même horizon, même WAPE)
avant de la retenir. Sur l'historique d'apprentissage, ses scores sont trop beaux.

### Garder chaque version de la prévision

Chaque lundi, on **ajoute** des lignes, on n'écrase rien :

```sql
-- Table de sortie (créée une fois)
CREATE TABLE IF NOT EXISTS `projet.prevision.prevision_hebdo` (
  date_origine DATE,      -- le lundi où la prévision a été faite
  semaine_cible DATE,
  horizon INT64,
  serie STRING,           -- 'web', 'encombrants'
  prevision FLOAT64,
  borne_basse FLOAT64,
  borne_haute FLOAT64,
  methode STRING,
  version_code STRING,    -- le commit git du script
  cree_le TIMESTAMP       -- l'heure du calcul : départage deux exécutions du même lundi
);
```

Le script `prevoir_hebdo.py --date-origine AAAA-MM-JJ` de l'exercice 04 fait la même chose dans un CSV.
Sur BigQuery, il écrit dans cette table (avec la bibliothèque `google-cloud-bigquery`), lancé chaque lundi
par un pipeline GitLab planifié (voir `gitlab.md`).

### Surveiller

```sql
-- Erreur des 4 dernières semaines closes, par série et par horizon, comparée au réel de la même série.
-- reel_hebdo(serie, semaine, valeur) : une ligne par série ('web', 'encombrants') et par semaine.
WITH derniere_version AS (                 -- si une prévision a été relancée, on garde la dernière
  SELECT * FROM `projet.prevision.prevision_hebdo`
  WHERE TRUE   -- BigQuery demande un WHERE avant QUALIFY
  QUALIFY ROW_NUMBER() OVER (PARTITION BY serie, semaine_cible, horizon ORDER BY cree_le DESC) = 1
)
SELECT p.serie, p.horizon,
       SUM(ABS(p.prevision - r.valeur)) / SUM(r.valeur) AS wape_4_semaines,
       AVG(p.prevision - r.valeur) AS biais,
       COUNTIF(r.valeur BETWEEN p.borne_basse AND p.borne_haute) / COUNT(*) AS part_dans_la_fourchette
FROM derniere_version p
JOIN `projet.prevision.reel_hebdo` r ON r.serie = p.serie AND r.semaine = p.semaine_cible
WHERE p.horizon IN (1, 12)
  -- semaines closes depuis au moins 7 jours, pour laisser passer les annulations tardives
  AND p.semaine_cible <  DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Paris'), ISOWEEK), INTERVAL 7 DAY)
  AND p.semaine_cible >= DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Paris'), ISOWEEK), INTERVAL 35 DAY)
GROUP BY p.serie, p.horizon;
```

Règle d'alerte simple, par série et par horizon : WAPE des 4 dernières semaines supérieure à 1,5 fois la WAPE
du backtest sur la période de note (même série, même horizon), ou biais du même signe 4 semaines de suite.
Attendez-vous à des alertes les semaines d'opérations (Black Friday) : regardez-les avant de changer de méthode.
La part dans la fourchette doit rester proche de 80 % : bien en dessous, la fourchette est trop étroite. Qui reçoit l'alerte, et qui décide de revenir à la règle simple : à écrire
dans `VALIDATION.md`.

## 2. Churn

### La photo à une date, paramétrée

```sql
-- photo.sql : une ligne par client, variables calculées AVANT @date_ref, cible APRÈS.
-- Lancer avec : bq query --use_legacy_sql=false --parameter=date_ref:DATE:2025-06-30 ...
WITH cmd AS (
  SELECT c.id_client, c.id_commande, c.date_commande,
         SUM(l.montant_ht - l.montant_retourne_ht) AS montant_net_ht
  FROM `projet.ventes.commandes` c
  JOIN `projet.ventes.lignes_commande` l USING (id_commande)
  WHERE c.statut <> 'ANNULEE' AND c.id_client IS NOT NULL
    AND c.date_commande BETWEEN DATE_SUB(@date_ref, INTERVAL 24 MONTH) AND DATE_ADD(@date_ref, INTERVAL 6 MONTH)
  GROUP BY c.id_client, c.id_commande, c.date_commande
),
avant AS (
  SELECT id_client,
         DATE_DIFF(@date_ref, MAX(date_commande), DAY) AS recence_jours,
         COUNTIF(date_commande > DATE_SUB(@date_ref, INTERVAL 365 DAY)) AS nb_commandes_12m,
         COUNT(*) AS nb_commandes_24m,
         SUM(IF(date_commande > DATE_SUB(@date_ref, INTERVAL 365 DAY), montant_net_ht, 0)) AS montant_12m_ht
  FROM cmd WHERE date_commande <= @date_ref
  GROUP BY id_client
),
mails AS (   -- ouvertures et clics des 90 jours AVANT la date de référence (date d'envoi, pas date de lecture)
  SELECT id_client,
         COUNT(*) AS nb_emails_recus_90j,
         COUNTIF(ouvert) AS nb_ouvertures_90j,
         COUNTIF(clique) AS nb_clics_90j
  FROM `projet.crm.emails`
  WHERE date_envoi > DATE_SUB(@date_ref, INTERVAL 90 DAY) AND date_envoi <= @date_ref
  GROUP BY id_client
),
apres AS (
  SELECT DISTINCT id_client
  FROM cmd
  WHERE date_commande > @date_ref AND date_commande <= DATE_ADD(@date_ref, INTERVAL 6 MONTH)
)
SELECT a.*,
       IFNULL(m.nb_emails_recus_90j, 0) AS nb_emails_recus_90j,
       IFNULL(m.nb_ouvertures_90j, 0) AS nb_ouvertures_90j,
       IFNULL(m.nb_clics_90j, 0) AS nb_clics_90j,
       @date_ref AS date_reference,
       IF(p.id_client IS NULL, 1, 0) AS perdu_6m
FROM avant a
LEFT JOIN mails m USING (id_client)
LEFT JOIN apres p USING (id_client);
```

Chaque colonne doit être **calculée à la date de référence** : jamais une colonne « du jour » (date de dernière
commande, statut du client, inscription aux e-mails telle qu'elle est aujourd'hui). C'est la fuite de l'exercice 05.
Pour les e-mails : si la table ne garde pas les envois aux clients désinscrits depuis, les anciennes photos
sous-comptent leurs ouvertures (question à poser, voir `a-demander.md`). Une ouverture est mal mesurée
(certaines messageries ouvrent seules les e-mails) : le clic est plus fiable.

### Apprendre sur une photo, tester sur la suivante

```sql
CREATE OR REPLACE MODEL `projet.churn.m_logreg`
OPTIONS (
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['perdu_6m'],
  auto_class_weights = TRUE,
  enable_global_explain = TRUE,
  data_split_method = 'NO_SPLIT'          -- on découpe nous-mêmes, par date
  -- Sans cette ligne, BigQuery ML découpe AU HASARD (AUTO_SPLIT) : c'est le découpage non temporel à éviter.
) AS
SELECT * EXCEPT (id_client, date_reference)
FROM `projet.churn.photos`
WHERE date_reference = DATE '2024-12-31';

-- Test sur la photo suivante, jamais vue
SELECT * FROM ML.EVALUATE(MODEL `projet.churn.m_logreg`,
  (SELECT * EXCEPT (id_client, date_reference) FROM `projet.churn.photos`
   WHERE date_reference = DATE '2025-06-30'));
```

Comparer à la règle simple **à liste de même taille** : combien de vrais perdus parmi les N premiers, pour le
modèle et pour la règle (une requête `ORDER BY ... LIMIT N` sur chacun).

### La liste du mois

```sql
SELECT id_client, predicted_perdu_6m_probs
FROM ML.PREDICT(MODEL `projet.churn.m_logreg`,
  (SELECT * FROM `projet.churn.photos` WHERE date_reference = DATE '2025-12-31'));
```

La « raison principale » par client, pour le CRM :

```sql
SELECT id_client, predicted_perdu_6m,
       top_feature_attributions[OFFSET(0)].feature AS raison_principale
FROM ML.EXPLAIN_PREDICT(MODEL `projet.churn.m_logreg`,
  (SELECT * FROM `projet.churn.photos` WHERE date_reference = DATE '2025-12-31'),
  STRUCT(3 AS top_k_features));
```

Écrire le résultat dans `scores_churn(id_client, date_reference, score, rang, version_modele)` en ajoutant des
lignes chaque mois. Six mois plus tard, comparer les scores aux départs constatés : c'est la seule vraie mesure.

### Auditer le modèle déjà en place

Avant de construire un nouveau modèle, faites auditer l'actuel. Les questions, dans l'ordre :

1. **Comment a-t-il été découpé ?** `bq show --format=prettyjson --model projet:churn:<modele>` : lisez
   `dataSplitMethod`. `AUTO_SPLIT` ou `RANDOM` = découpage au hasard, le score annoncé est trop optimiste.
2. **Avec quelles variables ?** `SELECT * FROM ML.FEATURE_INFO(MODEL ...)` : la liste exacte des colonnes.
   Pour chacune, d'où vient-elle et à quelle date est-elle connue ? (voir la liste de l'auditeur ci-dessous)
3. **Quelle variable domine ?** `SELECT * FROM ML.GLOBAL_EXPLAIN(MODEL ...)` (si `enable_global_explain`).
   Une variable qui écrase toutes les autres est suspecte : mesurez son AUC seule.
4. **Que vaut-il sur une photo ultérieure ?** Reconstruisez une photo propre à une date postérieure à
   l'apprentissage, et comparez au tri par récence, à liste de même taille.

Donnez ces quatre réponses au sous-agent `auditeur-fuite` avec la requête SQL qui a construit la table
d'apprentissage : il rendra son tableau comme dans l'exercice 05.

### L'auditeur de fuites, sur BigQuery

Le sous-agent `auditeur-fuite` du kit marche sur DuckDB. Sur BigQuery, donnez-lui la même liste de contrôles :
1. Pour chaque colonne, à quelle date est-elle connue ? Preuve : sa valeur maximale comparée à la date de référence.
2. Le découpage est-il par date, pas au hasard ?
3. Des retours ou annulations enregistrés **après** la date de référence entrent-ils dans les variables ?
4. La table des e-mails ne contient-elle que les inscrits d'aujourd'hui ?
5. Les clients anonymisés depuis manquent-ils aux anciennes photos (biais du survivant) ?

## 3. BigQuery ML ou Python ?

| Critère | BigQuery ML | Python (comme dans le kit) |
|---|---|---|
| Où sont les données | Elles ne sortent pas de BigQuery | Il faut les extraire (coût, données personnelles) |
| Qui maintient | Quelqu'un qui lit le SQL | Quelqu'un qui lit le Python |
| Planifier | Requête planifiée BigQuery | Pipeline GitLab planifié |
| Modèles | Régression logistique, arbres boostés, ARIMA_PLUS | Tout scikit-learn, statsmodels... |
| Expliquer un score | `ML.EXPLAIN_PREDICT` | à coder |

Règle simple : si le modèle tient dans `LOGISTIC_REG` ou `ARIMA_PLUS(_XREG)` et que les données sont déjà dans
BigQuery, commencer par BigQuery ML.
