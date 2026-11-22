---
name: documenter-table
description: Rédige ou complète la fiche d'une table dans semantique/tables/ selon les pratiques d'un catalogue de données - granularité prouvée, jointures mesurées, historique ou état du jour, données personnelles, contrôles à relancer - au format de semantique/README.md, puis demande validation avant d'écrire. À utiliser quand on veut documenter une table de la base de formation.
argument-hint: "[nom_de_table]"
---

# Documenter une table

Table à documenter : $ARGUMENTS (si rien n'est indiqué, demande laquelle).

Une fiche de table suit les pratiques d'un catalogue de données : dire d'où vient la table et ce qu'une
ligne représente, prouver chaque affirmation par une requête, séparer le constaté du supposé, et laisser
des contrôles qu'on pourra relancer à chaque mise à jour.

## Étapes

1. **Lire le format attendu** : `semantique/README.md` et la fiche exemple `semantique/tables/lignes_commande.md`.
   Lire aussi la fiche existante de la table (souvent vide) et `semantique/metriques.yml`.
2. **Lire le schéma** : `uv run python outils/requete.py --tables` (ou une requête sur `information_schema.columns`).
3. **Regarder les données** (lecture seule, avec `uv run python outils/requete.py "..."`) :
   - nombre de lignes ; un échantillon de 10 lignes ;
   - pour chaque colonne : part de valeurs vides, nombre de valeurs distinctes, minimum et maximum
     (dates, montants), valeurs possibles quand il y en a peu ;
   - **la granularité** : tester la clé supposée (`COUNT(*)` contre `COUNT(DISTINCT ...)`) ;
   - **les jointures** : pour chaque clé étrangère supposée, combien de lignes trouvent leur correspondance ?
   - **le temps** : période couverte, dernière date présente, fuseau horaire des dates ; la table garde-t-elle
     l'historique, ou seulement l'état du jour ? (une colonne « statut » ou « dernière date » est une valeur
     du jour : elle ne dit pas ce qu'on savait à une date passée) ;
   - **les données personnelles** : quelles colonnes identifient une personne (nom, e-mail, adresse) ?
   - si la table contient un agrégat (montant, compteur), **comparer son total à la définition de
     `metriques.yml`** et expliquer tout écart.
4. **Rédiger la fiche** au format exact du README (8 sections, dans l'ordre), avec le statut `BROUILLON`.
   Distinguer clairement ce qui est **constaté** (chiffres à l'appui) de ce qui est **supposé** (à confirmer
   par le métier : origine, fréquence de mise à jour, propriétaire). Lister les pièges trouvés.
   Dans « Suivi », écrire les contrôles à relancer (clé unique, colonnes jamais vides, valeurs attendues,
   jointures complètes), chacun sous forme d'une requête qui doit renvoyer 0 ligne ou un nombre connu.
   Chaque exemple de requête de la section 7 doit avoir été exécuté, avec son résultat noté.
5. **Montrer la fiche et demander validation** : afficher le projet de fiche, la liste des contrôles faits
   avec leurs résultats, et les questions à poser au métier. **Ne rien écrire avant le « oui » de la personne.**
6. Après validation : écrire `semantique/tables/<table>.md`, puis résumer en trois lignes ce qui a été ajouté.

## Règles

- Ne jamais modifier les données ni `donnees/brutes/`.
- Chaque chiffre de la fiche (total, part, écart en %) vient d'une requête exécutée dans cette session, dont le
  résultat a été affiché. Pas de chiffre estimé de tête : s'il manque, lancer la requête ou écrire « à mesurer ».
- Une fiche courte : moins de 120 lignes. Le détail des contrôles va dans la section « Suivi », sous forme de requêtes.
- Ne pas lire `exercices/` ni `donnees/generer_donnees.py` : documenter et calculer à partir des données.
- Français simple, phrases courtes ; expliquer les termes techniques (granularité, clé, jointure) la première fois.
