---
name: entrainer-modele
description: Transforme un besoin d'apprentissage automatique décrit en une phrase (prévoir un volume, repérer des clients) en un script Python qui prépare les données, entraîne un modèle, le compare à une règle simple et affiche l'erreur. Écrit le script dans travail/<prénom>/modeles/<nom>/ et le lance. Version courte de /modeliser, pour un premier essai.
argument-hint: "[le besoin, en une phrase]"
---

# Entraîner un premier modèle

Besoin : $ARGUMENTS (si rien n'est donné, demander le besoin en une phrase).

Si le prénom de la personne n'est pas connu, le demander (il sert au dossier `travail/<prénom>/`).

Pourquoi cette skill : passer d'une phrase à un premier résultat chiffré en quelques minutes, toujours de la
même façon, et voir tout de suite si le modèle fait mieux qu'une règle simple. Ce n'est pas une validation :
la validation se fait ensuite avec `/valider-modele`.

## Étapes

1. **Cadrer en cinq lignes**, après avoir lu `semantique/` (les fiches des tables utiles et `metriques.yml`) :
   - **Type de problème** : prévision d'une série dans le temps, classification (oui ou non) ou régression
     (un nombre).
   - **Cible** : la colonne ou le calcul exact, son unité, et l'horizon (combien de temps à l'avance).
   - **Une ligne** : ce que représente une ligne du jeu de données (une semaine, un client à une date).
   - **Variables** : les colonnes utilisées pour prédire, toutes **connues à la date où l'on fait la prévision**.
   - **Règle simple à battre** : pour une prévision, « même semaine l'an dernier ». Pour des clients,
     « pas d'achat depuis 270 jours ». Pour une régression, la moyenne de la période d'apprentissage.
   Montrer ces cinq lignes, dire le nom du dossier, et attendre l'accord de la personne. Une ambiguïté qui
   change le résultat : poser une seule question. Sinon, choisir l'option la plus simple et le dire.
2. **Écrire le script** `travail/<prénom>/modeles/<nom-court>/entrainer.py`, court et commenté en français :
   - lire la base en lecture seule : `duckdb.connect("donnees/ecommerce.duckdb", read_only=True)`.
   - **découper dans le temps** : apprentissage sur la période ancienne, test sur la période récente, jamais
     au hasard.
   - calculer la règle simple, puis entraîner **un** modèle de scikit-learn (par exemple
     `HistGradientBoostingRegressor` ou `HistGradientBoostingClassifier`), avec une graine fixe.
   - afficher : le nombre de lignes d'apprentissage et de test, les dates de coupure, la mesure de la règle et
     celle du modèle sur la même période de test, et les variables qui pèsent le plus.
   - prévision : erreur moyenne en pourcentage (WAPE : écart absolu total divisé par le réel total).
   - clients : précision et rappel pour une liste de même taille que celle de la règle.
   - écrire les mêmes chiffres dans `resultats.md`, à côté du script.
3. **Lancer le script** depuis le dossier du kit : `uv run python travail/<prénom>/modeles/<nom-court>/entrainer.py`.
   S'il échoue, lire l'erreur, corriger, relancer, et dire ce qui a été corrigé.
4. **Lire le résultat avec méfiance** :
   - le modèle ne bat pas la règle : le dire simplement, c'est un résultat.
   - le modèle est beaucoup trop bon (erreur divisée par plus de deux, ou précision au-dessus de 95 %) :
     chercher d'abord une fuite de données (une variable connue après la date), proposer le sous-agent
     `auditeur-fuite`, et ne pas annoncer le résultat comme acquis.
5. **Expliquer en cinq phrases** : ce que fait le script, ce que dit le chiffre, et ce qu'il ne dit pas encore.

Ne jamais modifier `donnees/`. Ne pas chercher le meilleur modèle : un seul modèle, une seule règle.

## Ce que tu affiches à la fin

```
Modèle <nom-court> : <besoin en une phrase>.
✓ Script : travail/<prénom>/modeles/<nom-court>/entrainer.py
✓ Données : <n> lignes d'apprentissage (<dates>), <n> lignes de test (<dates>)
✓ Règle simple (<la règle>) : <mesure>
✓ Modèle (<nom du modèle>) : <mesure>
Verdict : <le modèle fait mieux / ne fait pas mieux / trop beau, à vérifier>
```

Puis la suite en une ligne : « Pour décider si on peut s'en servir : /valider-modele. Pour comprendre le
code : /expliquer. »
