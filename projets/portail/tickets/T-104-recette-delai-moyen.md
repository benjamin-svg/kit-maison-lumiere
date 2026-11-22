# T-104 : Retour de recette - le délai moyen affiché en bas de page est faux

- Type : anomalie (retour de recette)
- Signalé par : acheteuse prêt-à-porter, pendant la recette de la version 1.2 du portail
- Priorité : moyenne

## Contexte

Depuis la version 1.2, la page « Délais fournisseurs » affiche sous le tableau le délai moyen des
fournisseurs affichés. Les acheteurs s'en servent pour comparer les pays entre eux.

## Ce que j'ai fait

1. Ouvrir `/delais-fournisseurs?pays=Portugal`.
2. Recopier les cinq délais moyens dans Excel et faire la moyenne.

## Ce que j'ai constaté

- La page affiche « Délai moyen des fournisseurs affichés : 12 j ».
- Excel donne **12,6 jours** : (9 + 21 + 14 + 11 + 8) / 5.
- Avec un pays qui n'existe pas (`?pays=Japon`), la page affiche « 0 j », ce qui laisse croire à un délai nul.

## Critères d'acceptation

1. Le délai moyen est affiché avec une décimale et une virgule : « 12,6 j » pour le Portugal.
2. Quand aucun fournisseur n'est affiché, la page affiche « Délai moyen des fournisseurs affichés : - »
   au lieu de « 0 j ».
3. Le calcul reste fait sur les seuls fournisseurs affichés (avec le filtre pays).
4. Les tests existants passent toujours, et de nouveaux tests couvrent les critères 1 à 3.
