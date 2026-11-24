# T-100 : Annoncer l'application de traduction sur la page d'accueil

- Type : évolution
- Demandé par : équipe e-commerce
- Priorité : normale

## Contexte

Un projet de traduction des fiches produits démarre (du français vers l'allemand et le néerlandais).
Il doit apparaître sur la page d'accueil du portail, comme les autres projets en cours.
L'équipe veut aussi voir d'un coup d'œil combien d'applications sont déjà en service.

## Demande

Ajouter l'application « Traduction des fiches produits » sur la page d'accueil, et afficher sous les cartes
le nombre d'applications et le nombre d'applications en service.

## Critères d'acceptation

1. La page d'accueil affiche une carte « Traduction des fiches produits », avec la description
   « Traduction des fiches en allemand et en néerlandais, avec le ton de la marque (projet en cours). »,
   le statut « à venir » et sans lien.
2. Sous les cartes, la page d'accueil affiche « 5 applications, dont 2 en service ». Ces deux nombres sont
   calculés à partir de la liste des applications, pas écrits dans le code.
3. `/api/applications` renvoie aussi la nouvelle application.
4. Des tests automatisés couvrent les critères 1 à 3, et tous les tests existants passent toujours.
