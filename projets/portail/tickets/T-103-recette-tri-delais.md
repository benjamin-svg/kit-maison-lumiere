# T-103 : Retour de recette - le tri des délais fournisseurs est faux

- Type : anomalie (retour de recette)
- Signalé par : acheteuse prêt-à-porter, pendant la recette de la version 1.2 du portail
- Priorité : haute (bloque la mise en production)

## Contexte

La page « Délais fournisseurs » annonce : « Fournisseurs classés du délai moyen le plus long au plus court ».
Les acheteurs s'en servent pour repérer en premier les fournisseurs qui demandent d'anticiper.

## Ce que j'ai fait

1. Ouvrir `/delais-fournisseurs`, sans filtre.
2. Regarder les premières lignes du tableau.

## Ce que j'ai constaté

- En tête de liste : **Atelier Douro** (9 jours), puis **Chemiserie Braga** (8 jours), puis Rotins de Java (75 jours).
  Ces deux fournisseurs portugais sont pourtant les plus rapides de toute la liste.
- Avec le filtre pays « Portugal », même chose : Atelier Douro (9) et Chemiserie Braga (8) passent avant
  Tissages de Guimarães (21 jours).
- Avec le filtre pays « France », l'ordre m'a semblé correct. Je ne comprends pas pourquoi.

## Ce que j'attendais

Rotins de Java (75 jours) en premier, puis Ébénisterie Vosgienne (68), Bois et Hêtre (60), etc.,
et les fournisseurs les plus rapides (Chemiserie Braga, 8 jours) en dernier. Le même ordre dans l'API
`/api/delais-fournisseurs`.

## Critères d'acceptation

1. La page et l'API classent les fournisseurs par délai moyen décroissant, en comparant des nombres.
2. Le tri reste juste après un filtre par pays.
3. À délai égal, l'ordre est alphabétique sur le nom du fournisseur (ordre stable et prévisible).
4. Un test automatisé reproduit l'anomalie : il échoue avant la correction et passe après.
