# T-102 : Ajouter le panier moyen et les annulations au suivi des commandes du jour

- Type : évolution
- Demandé par : responsable e-commerce
- Priorité : haute

## Contexte

Chaque matin, la responsable e-commerce regarde la page « Suivi des commandes du jour ».
Elle voit le nombre de commandes, d'articles et le CA net HT par canal, mais elle doit recalculer
le panier moyen à la main, et elle ne voit pas les commandes annulées, qui augmentent pendant
les grosses opérations (Black Friday).

## Demande

Ajouter deux colonnes au tableau de la page et à l'API `/api/commandes-du-jour` :

- **Panier moyen HT** : CA net HT divisé par le nombre de commandes non annulées (arrondi à 2 décimales) ;
- **Commandes annulées** : nombre de commandes au statut `ANNULEE` ce jour-là sur ce canal.

## Critères d'acceptation

1. Le CA net HT et le nombre de commandes restent calculés **hors commandes annulées**, comme aujourd'hui.
2. Le panier moyen respecte la définition de `semantique/metriques.yml` (métrique `panier_moyen_ht`,
   à compléter si elle ne l'est pas encore).
3. Un canal qui n'a que des commandes annulées ce jour-là apparaît quand même, avec 0 commande,
   un CA de 0, un panier moyen vide (pas de division par zéro) et son nombre d'annulations.
4. L'API renvoie les nouveaux champs `panier_moyen_ht` et `nb_commandes_annulees`.
5. Les tests existants passent toujours, et de nouveaux tests couvrent les critères 1, 3 et 4
   avec la base de test de `conftest.py` (complétée si besoin).
