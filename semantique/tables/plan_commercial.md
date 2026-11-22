# Table `plan_commercial`

Statut : **VALIDEE** (deuxième fiche complète, utile pour la prévision)

## Rôle

Le plan des opérations commerciales **tel qu'il était connu à chaque date de publication**. Le plan de l'année N
est publié à la mi-novembre de l'année N-1 ; quand une opération est déplacée en cours d'année, une nouvelle
version est publiée. La table contient aussi le plan 2026, publié le 17/11/2025.

À utiliser pour une **prévision** : à une date D, on ne connaît que les versions publiées au plus tard le jour D.

Origine : tableau du marketing, saisi à chaque publication du plan ; les anciennes versions sont gardées
(c'est une table **historisée**). Aucune donnée personnelle.
Pour un **bilan** d'opération (ce qui s'est vraiment passé), utiliser `calendrier_commercial`, qui donne les
dates réalisées.

## Granularité

**Une ligne = une version d'une opération.** Une opération jamais déplacée a une ligne ; une opération
déplacée en a deux (versions 1 et 2).

## Clés

- Clé primaire : (`id_operation`, `version`).
- `id_operation` -> `calendrier_commercial.id_operation` pour les opérations 2023 à 2025 (1 à 30).
  Les opérations 2026 (31 à 40) ne sont pas encore dans `calendrier_commercial`.

## Jointures autorisées

| Avec | Condition | Effet sur le nombre de lignes |
|---|---|---|
| `calendrier_commercial` | `p.id_operation = c.id_operation` | **duplique** les opérations déplacées : filtrer d'abord une version |
| une série par jour ou par semaine | `jour BETWEEN p.date_debut AND p.date_fin`, après avoir gardé la version connue à D | peut dupliquer si deux opérations se chevauchent |

## Colonnes utiles

| Colonne | Type | Signification |
|---|---|---|
| `id_operation` | entier | identifiant de l'opération (le même pour toutes ses versions) |
| `version` | entier | 1 pour le plan annuel, 2 après un déplacement |
| `date_version` | date | jour où cette version a été publiée |
| `libelle` | texte | par exemple « Vente privée 2 2025 » |
| `type_operation` | texte | `SOLDES`, `BLACK_FRIDAY`, `VENTE_PRIVEE`, `LIVRAISON_OFFERTE`, `FETE_DES_MERES`, `RENTREE`, `NOEL` |
| `canaux` | texte | `TOUS` ou `WEB` |
| `date_debut`, `date_fin` | date | dates prévues dans cette version (bornes incluses) |

## Pièges connus

- **Prendre la dernière version pour un backtest est une fuite de données** : on utiliserait une date qu'on
  ne connaissait pas encore. Exemple : pour une prévision faite le 15/08/2025, la vente privée d'octobre 2025
  était prévue du 01/10 au 05/10 (plan annuel). Son déplacement au 08/10 n'a été publié que le 01/09/2025.
- Quatre opérations ont été déplacées : vente privée 2 2024, vente privée 2 2025, livraison offerte 2 2025,
  vente privée 1 2026.
- Le Black Friday et Noël se chevauchent le 1er décembre 2025 ; les livraisons offertes et la fête des mères
  peuvent aussi se chevaucher.

## Exemples de requêtes validées

Le plan connu le lundi 15/09/2025, pour les opérations qui commencent après cette date :

```sql
SELECT id_operation, libelle, date_debut, date_fin
FROM plan_commercial
WHERE date_version <= DATE '2025-09-15' AND date_debut >= DATE '2025-09-15'
QUALIFY ROW_NUMBER() OVER (PARTITION BY id_operation ORDER BY version DESC) = 1
ORDER BY date_debut;
```

Résultat contrôlé : 4 opérations (vente privée 2 2025 du 08/10 au 12/10, livraison offerte 2 2025 encore prévue
du 12/11 au 14/11, Black Friday 2025, Noël 2025).

## Suivi

- Propriétaire des données : Marketing e-commerce (fictif)
- Validée par : Marketing e-commerce (fictif)
- Date : 2025-12-15
- Contrôles à relancer à chaque mise à jour : (`id_operation`, `version`) unique ; `date_debut` au plus tard
  `date_fin` ; `date_version` antérieure à `date_debut` ; aucune version publiée après la date d'extraction.
