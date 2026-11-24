# Démonstration 5 : la modélisation (10 min)

Ce qu'on voit : vous décrivez un besoin en une phrase. La skill `/entrainer-modele` le cadre en cinq lignes,
écrit un script Python, le lance, et compare le modèle à une règle simple. Vous lisez le code produit,
vous ne l'écrivez pas.

## 1. Une prévision

> « /entrainer-modele Prévoir le nombre de commandes web de chaque semaine, une semaine à l'avance. »

À voir :
- le cadrage : type de problème, cible, ce qu'est une ligne, les variables, la règle à battre (« même semaine
  l'an dernier »). Validez-le.
- le script dans `travail/<prénom>/modeles/`, lancé avec `uv run python`.
- le découpage dans le temps : on apprend sur les semaines anciennes et on teste sur les récentes.
- l'erreur de la règle et celle du modèle, sur les mêmes semaines.

## 2. Des clients qui partent

> « /entrainer-modele Repérer les clients qui ne commanderont plus dans les six prochains mois, à partir de la photo des clients au 30 juin 2025. »

À voir : la règle à battre (« pas d'achat depuis 270 jours »), la précision et le rappel pour une liste de même
taille. Sur le kit, le modèle fait à peu près aussi bien que la règle, pas mieux : c'est un résultat, et c'est pour
cela qu'on mesure toujours la règle d'abord. Si au contraire le résultat était trop beau (précision au-dessus de
95 %), demandez : « Demande au sous-agent auditeur-fuite de vérifier les variables. »

## 3. Comprendre le code

> « /expliquer le script de la prévision »

À voir : chaque bloc du script expliqué en français.

## Pour aller plus loin

La version longue de cette démonstration : [l'exercice 04](../exercices/04-ml-prevision.md) (prévision) ou [l'exercice 05](../exercices/05-ml-churn.md) (churn), 1 h chacun : cadrer avec /modeliser, tester dans l'ordre du temps, chercher une fuite, valider avec /valider-modele.

## Dans votre cas

| Qui | Cas | La phrase à donner | La règle à battre |
|---|---|---|---|
| Olivier | Prévision des commandes web | « Prévoir les commandes web par semaine, à 1 semaine et à 3 mois, avec le plan commercial. » | même semaine l'an dernier |
| Augustin | Churn | « Prédire les clients qui seront inactifs dans 6 mois. » Puis comparer au modèle Dataiku, avant BigQuery ML. | pas d'achat depuis 9 mois |
| Olivier | Traduction | pas de modèle à entraîner : Claude traduit avec le guide de ton, le glossaire et des traductions passées | la part du texte corrigée par le relecteur |
| Maxime | Visuels produits | pas de modèle à entraîner : un script pilote des outils de détourage et de recadrage | une personne valide avant publication |
| Maxime | Délais ORLI | pas de modèle : un script classique fait toujours la même chose | - |
| Céline | Analyses BigQuery | pas de modèle : des requêtes SQL vérifiées | - |
