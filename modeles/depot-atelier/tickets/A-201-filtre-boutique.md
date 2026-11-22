# A-201 : Filtrer les alertes par boutique

- Type : évolution
- Demandé par : responsable des boutiques
- Priorité : haute

## Contexte

Chaque responsable de boutique ne s'intéresse qu'à sa boutique. Aujourd'hui, la page affiche les alertes
de toutes les boutiques mélangées.

## Demande

Ajouter un filtre par boutique sur la page d'accueil et sur l'API `/api/alertes`.

## Critères d'acceptation

1. `/api/alertes?boutique=Lille` ne renvoie que les alertes de Lille.
2. Le filtre ne tient pas compte des majuscules : `boutique=lille` donne le même résultat.
3. Sans filtre, toutes les alertes restent affichées, comme aujourd'hui.
4. Une boutique inconnue renvoie une liste vide, sans erreur.
5. La page d'accueil propose une liste déroulante des boutiques, triée, sans doublon.
6. Les tests existants passent toujours, et de nouveaux tests couvrent les critères 1 à 5.
