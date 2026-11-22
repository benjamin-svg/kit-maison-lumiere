# A-202 : Retour de recette - un article au seuil n'apparaît pas dans les alertes

- Type : anomalie (retour de recette)
- Signalé par : responsable de la boutique de Lyon
- Priorité : haute

## Ce que j'ai constaté

La robe plissée en lin (R-1001) a un stock de 4 à Lyon, et son seuil d'alerte est de 4. Elle n'apparaît pas
dans les alertes. Même chose pour le coussin lin lavé à Nantes (stock 6, seuil 6).

## Ce que j'attendais

La règle de l'entreprise est : « on réapprovisionne quand le stock atteint le seuil ». Un article dont le stock
est égal au seuil doit donc apparaître dans les alertes.

## Critères d'acceptation

1. Un article dont le stock est égal au seuil d'alerte apparaît dans les alertes.
2. Un test reproduit l'anomalie et échoue avant la correction.
3. Les tests existants passent toujours.
