# T-101 : Filtrer la page « Délais fournisseurs » par famille de produits

- Type : évolution
- Demandé par : équipe approvisionnement
- Priorité : normale

## Contexte

Les acheteurs consultent la page « Délais fournisseurs » pour préparer leurs commandes.
Aujourd'hui, on ne peut filtrer que par pays. L'acheteuse « maison » doit parcourir toute la liste
pour retrouver les fournisseurs de linge de maison, de mobilier et de décoration.

## Demande

Ajouter un filtre par famille de produits sur la page et sur l'API, utilisable seul ou avec le filtre par pays.

## Critères d'acceptation

1. La page `/delais-fournisseurs` propose une liste déroulante « Famille » (valeur « Toutes » par défaut),
   construite à partir des familles présentes dans le fichier, sans doublon, par ordre alphabétique.
2. `/delais-fournisseurs?famille=pull` n'affiche que les fournisseurs de la famille `pull`.
3. `/api/delais-fournisseurs?famille=pull` renvoie la même sélection au format JSON.
4. Le filtre ne tient pas compte des majuscules : `famille=Pull` donne le même résultat que `famille=pull`.
5. Les filtres se combinent : `?pays=France&famille=pull` ne renvoie que les fournisseurs français de pulls.
6. Une famille inconnue renvoie une liste vide et la page affiche « 0 fournisseur(s) », sans erreur.
7. Des tests automatisés couvrent les critères 2 à 6, et tous les tests existants passent toujours.
