# Couche sémantique de Maison Lumière

Ce dossier dit **ce que veulent dire les données** : à quoi sert chaque table, à quel niveau de détail
elle est tenue, comment la joindre aux autres, quels pièges éviter, et comment calculer les indicateurs
de l'entreprise (« métriques ») de façon unique.

Sans ce dossier, Claude (comme un nouvel analyste) devine : il prend la table qui a l'air la plus simple,
et il peut se tromper sans le savoir. Avec ce dossier, il suit les définitions validées par le métier.

**Règle du kit : avant d'écrire une requête SQL, lire ce dossier.**

## Contenu

- `tables/<table>.md` : une fiche par table. `lignes_commande.md` et `plan_commercial.md` sont complètes ;
  les autres sont à compléter pendant l'exercice 03 (skill `/documenter-table`).
- `metriques.yml` : les définitions des indicateurs. Deux sont validées (`ca_net_ht`, `nb_commandes`),
  les autres portent leur statut (`A_COMPLETER` au départ, puis `BROUILLON`, puis `VALIDEE`) :
  c'est le statut, pas ce paragraphe, qui dit où en est chaque métrique.

## Format d'une fiche de table

Chaque fiche suit le même plan, dans cet ordre :

1. **Rôle et origine** : à quoi sert la table, en une ou deux phrases, et pour quelles questions l'utiliser (ou non).
   D'où elle vient (logiciel source), à quelle fréquence elle est mise à jour, et si elle garde l'historique
   ou seulement l'état du jour (une table « état du jour » ne dit pas ce qu'on savait à une date passée).
2. **Granularité** : ce que représente une ligne (« une ligne = une ligne de commande »). C'est la notion la plus
   importante : elle dit ce qu'on peut additionner sans doublon.
3. **Clés** : la clé primaire (unique par ligne) et les clés étrangères.
4. **Jointures autorisées** : avec quelles tables, sur quelles colonnes, et ce que la jointure fait au nombre de lignes.
5. **Colonnes utiles** : nom, type, signification, valeurs possibles, unité ; fuseau horaire des dates ;
   et si la colonne est une donnée personnelle (nom, e-mail, adresse... : accès et usages limités).
6. **Pièges connus** : ce qui a déjà trompé quelqu'un.
7. **Exemples de requêtes validées** : des requêtes relues et dont le résultat a été contrôlé.
8. **Suivi** : le propriétaire des données (qui répond de leur contenu), qui a validé la fiche, et quand ;
   les contrôles à relancer à chaque mise à jour (clé unique, colonnes jamais vides, valeurs attendues,
   jointures complètes). Une fiche non validée porte le statut `BROUILLON`.

## Format d'une métrique (`metriques.yml`)

```yaml
nom_de_la_metrique:
  statut: VALIDEE            # ou A_COMPLETER, BROUILLON
  libelle: ...               # le nom affiché dans un rapport
  definition: ...            # une phrase en français, compréhensible par le métier
  formule_sql: ...           # une requête SQL complète, qu'on peut exécuter telle quelle (paramètres
                             # :date_debut, :date_fin ou :date_obs, à remplacer par des dates), testée
                             # sur la base avant d'être écrite
  exemple: ...               # le résultat pour une vraie période, qui sert de test : la formule doit le redonner
  additivite: ...            # peut-on additionner les jours, les canaux ? (non pour un panier moyen ou un
                             # nombre de clients actifs : on recalcule sur la période entière)
  tables: [...]              # tables nécessaires
  filtres: [...]             # conditions toujours appliquées
  date_de_rattachement: ...  # quelle date sert à placer l'indicateur dans le temps
  unite: ...
  pieges: [...]
  proprietaire: ...          # qui tranche en cas de désaccord
  valide_le: AAAA-MM-JJ
```

## Comment faire évoluer ce dossier

- Une nouvelle définition ou une correction passe par une relecture (comme du code) :
  branche git, modification, relecture, fusion.
- Une fiche ou une métrique au statut `BROUILLON` ne doit pas servir à un chiffre diffusé.
- Avant de valider une modification de `metriques.yml`, la faire relire par le sous-agent `relecteur`
  (chiffres des pièges recalculés, formule exécutée).
- Les formules sont écrites en SQL DuckDB. Sur BigQuery, la syntaxe change : demander à Claude de traduire la requête et de lister chaque différence.
- Quand une analyse révèle un nouveau piège, on l'ajoute à la fiche concernée.
