# Table `lignes_commande`

Statut : **VALIDEE** (exemple de fiche complète)

## Rôle

Le détail des articles de chaque commande : quel produit, en quelle quantité, à quel prix, avec quelle remise,
et ce qui a été retourné. **C'est la table de référence pour tout calcul de chiffre d'affaires**, de volume
d'articles, de remise ou de retour, par produit, famille, canal ou période.

À ne pas utiliser seule pour compter des commandes ou des clients : il faut passer par `commandes`.

Origine : extraction du site web, des magasins et de la marketplace, chargée chaque nuit (dans le kit :
extraction unique au 31/12/2025). La table donne **l'état au jour de l'extraction** : les retours d'une
commande sont ajoutés quand ils arrivent, jusqu'à plusieurs semaines après la commande. Pour reconstituer
ce qu'on savait à une date passée (prévision, churn), les retours récents ne sont pas encore connus.
Aucune donnée personnelle dans cette table.

## Grain

**Une ligne = un produit dans une commande.** Une commande de 3 produits différents a 3 lignes.
Une ligne peut porter une quantité de 2 (deux exemplaires du même produit).

## Clés

- Clé primaire : `id_ligne` (unique).
- Clés étrangères :
  - `id_commande` -> `commandes.id_commande` (toutes les lignes ont une commande) ;
  - `id_produit` -> `produits.id_produit` (toutes les lignes ont un produit connu).

## Jointures autorisées

| Avec | Condition | Effet sur le nombre de lignes |
|---|---|---|
| `commandes` | `l.id_commande = c.id_commande` | inchangé (plusieurs lignes pour une commande) |
| `produits` | `l.id_produit = p.id_produit` | inchangé |
| `clients` | via `commandes` : `c.id_client = cl.id_client` | inchangé, mais `id_client` peut être vide (voir pièges) |
| `calendrier_commercial` | `c.date_commande BETWEEN o.date_debut AND o.date_fin` | **peut dupliquer** si deux opérations se chevauchent : vérifier |

Jointure interdite : `emails` directement (aucune clé commune au bon grain).

## Colonnes utiles

| Colonne | Type | Signification |
|---|---|---|
| `id_ligne` | entier | identifiant de la ligne |
| `id_commande` | entier | commande d'appartenance |
| `id_produit` | entier | produit vendu |
| `quantite` | entier | nombre d'exemplaires (1 ou 2) |
| `prix_unitaire_ht` | décimal, euros HT | prix catalogue unitaire, avant remise |
| `remise_ht` | décimal, euros HT | remise totale de la ligne (soldes, Black Friday, ventes privées, promotions) |
| `montant_ht` | décimal, euros HT | `quantite * prix_unitaire_ht - remise_ht` : ce que le client a payé HT, avant retours |
| `quantite_retournee` | entier | exemplaires retournés (0 si aucun) |
| `montant_retourne_ht` | décimal, euros HT | montant HT remboursé au titre des retours |

Les statuts utiles sont dans `commandes.statut` : `LIVREE`, `EN_COURS` (commandes des derniers jours,
pas encore livrées), `ANNULEE`.

## Pièges connus

1. **Les commandes annulées ont des lignes.** Toujours joindre `commandes` et filtrer
   `c.statut <> 'ANNULEE'` pour un chiffre d'affaires ou un volume.
2. **Retours** : le CA net se calcule `montant_ht - montant_retourne_ht`. Les retours sont rattachés à la date
   de la commande d'origine, pas à la date du retour.
3. **HT et TTC** : `commandes.montant_ttc` est un montant TTC **qui inclut les frais de port**.
   Ne pas le mélanger avec `montant_ht`.
4. **Doublons après jointure** : après `JOIN commandes`, une colonne de `commandes` (par exemple `montant_ttc`)
   est répétée sur chaque ligne de la commande. La sommer multiplie le montant par le nombre de lignes.
   Pour compter des commandes, utiliser `COUNT(DISTINCT c.id_commande)`.
5. **Moyenne par ligne et moyenne par commande** : `AVG(montant_ht)` sur cette table donne le montant moyen
   d'une *ligne*, pas le panier moyen d'une *commande*.
6. **Client vide** : certaines commandes anciennes n'ont plus de client (`commandes.id_client` vide), à cause
   de l'anonymisation des clients inactifs. Le CA reste juste ; les analyses par client sont incomplètes.
7. **Commandes `EN_COURS`** : elles comptent dans le CA (la définition métier n'exclut que les annulées),
   mais leurs retours ne sont pas encore connus.

## Exemples de requêtes validées

CA net HT par mois et par canal (définition `ca_net_ht` de `metriques.yml`) :

```sql
SELECT DATE_TRUNC('month', c.date_commande) AS mois,
       c.canal,
       ROUND(SUM(l.montant_ht - l.montant_retourne_ht), 2) AS ca_net_ht
FROM lignes_commande l
JOIN commandes c ON c.id_commande = l.id_commande
WHERE c.statut <> 'ANNULEE'
GROUP BY ALL
ORDER BY mois, c.canal;
```

Taux de retour (en valeur) par famille de produits, sur le web, en 2024 :

```sql
SELECT p.famille,
       ROUND(100 * SUM(l.montant_retourne_ht) / SUM(l.montant_ht), 1) AS taux_retour_pct
FROM lignes_commande l
JOIN commandes c ON c.id_commande = l.id_commande
JOIN produits p ON p.id_produit = l.id_produit
WHERE c.statut <> 'ANNULEE' AND c.canal = 'WEB' AND YEAR(c.date_commande) = 2024
GROUP BY p.famille
ORDER BY taux_retour_pct DESC;
```

Contrôle de cohérence (doit renvoyer 0 ligne) : aucune ligne sans commande ni sans produit.

```sql
SELECT l.id_ligne
FROM lignes_commande l
LEFT JOIN commandes c ON c.id_commande = l.id_commande
LEFT JOIN produits p ON p.id_produit = l.id_produit
WHERE c.id_commande IS NULL OR p.id_produit IS NULL;
```

## Suivi

- Propriétaire des données : contrôle de gestion e-commerce
- Validée par : contrôle de gestion e-commerce
- Date : 2025-12-15
- Contrôles à relancer à chaque mise à jour : `id_ligne` unique et jamais vide ; la requête de cohérence
  ci-dessus renvoie 0 ligne ; `montant_retourne_ht` entre 0 et `montant_ht` ; `quantite` au moins 1.
