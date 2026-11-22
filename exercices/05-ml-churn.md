# Exercice 05 - Repérer les clients qui risquent de ne plus commander

## Objectif

Construire avec Claude un modèle de churn (perte de clients) qui bat un modèle de référence, en apprenant à se
méfier d'un résultat trop beau : trouver la fuite de données cachée dans la table de travail, valider le
modèle proprement, comprendre le biais créé par l'anonymisation des clients inactifs, et produire une liste
de ciblage utilisable.

Table de départ : `clients_churn_snapshot`, une photo des clients au **30 juin 2025** (date de référence),
avec la cible `perdu_6m` : 1 si le client n'a passé aucune commande non annulée du 01/07/2025 au 29/12/2025
(182 jours après la date de référence).

## Durée

1 heure en salle : étapes 1 à 5. Les étapes 6 et 7 se font en autonomie (ou lundi).

## Étape 1 - Cadrer (10 min)

Passez en mode plan (Maj+Tab), puis :

> « /modeliser Repérer, au 30 juin 2025, les clients qui ne commanderont plus dans les 6 mois, pour leur envoyer une offre de relance. Pars de la table clients_churn_snapshot. »

**À observer** : la cible, la date de référence, la fenêtre d'observation (le passé) et la fenêtre de la
cible (les 6 mois suivants), la population (qui est dans la photo, qui n'y est pas), la mesure de réussite
(combien de vrais perdus dans une liste de N clients). Validez le plan, sortez du mode plan.

## Étape 2 - Le modèle de référence (10 min)

> « Mesure le modèle de référence "un client est perdu s'il n'a pas acheté depuis 270 jours" sur clients_churn_snapshot : part des clients ciblés, matrice de confusion, taux de bonnes prédictions, précision, rappel. Explique chaque mesure en une phrase. »

## Étape 3 - Un premier modèle, avec toutes les colonnes (5 min)

> « Entraîne rapidement un modèle de classification sur clients_churn_snapshot en utilisant toutes les colonnes disponibles comme variables, avec un découpage aléatoire 70/30. Donne le taux de bonnes prédictions, la précision et le rappel, et compare au modèle de référence. »

**À observer** : le résultat est excellent. Trop excellent ? Vous savez par les slides qu'une fuite existe, et
Claude la soupçonnera peut-être tout de suite. Le but n'est pas la surprise : c'est de voir **quelle preuve**
il apporte (la date à laquelle chaque colonne est connue, le taux de bonnes prédictions obtenu avec chaque colonne prise seule), car c'est
cette preuve que vous referez lundi sur votre vrai modèle, où personne ne vous aura dit où est la fuite.

## Étape 4 - L'audit des fuites (15 min)

> « Ce résultat me paraît trop beau. Demande au sous-agent auditeur-fuite d'auditer la table clients_churn_snapshot et le modèle de l'étape 3. »

**À observer** : l'auditeur vérifie, pour chaque colonne, à quelle date elle est connue, et mesure le lien
de chaque colonne prise seule avec la cible. Il doit trouver la colonne qui « connaît l'avenir », et signaler
le découpage aléatoire.

## Étape 5 - Le vrai modèle et sa validation (20 min)

> « Retire la ou les colonnes signalées. Pour un test honnête, construis une deuxième photo au 31 décembre 2024 à partir des tables commandes, lignes_commande, clients et emails, avec les mêmes définitions de colonnes (sans la colonne fautive) ; sa cible : aucune commande non annulée du 01/01/2025 au 30/06/2025 inclus, pour qu'elle soit close avant la photo de test. Entraîne sur cette photo et teste sur celle du 30 juin 2025. Commence par une régression logistique. Compare à deux références : la règle des 270 jours, et le simple classement des clients par ancienneté de leur dernier achat. Donne la précision et le rappel pour une liste de même taille que celle de la règle, et le nombre de vrais perdus parmi les 1 000 clients les plus à risque qui ont acheté il y a moins de 270 jours. »

Puis :

> « /valider-modele travail/<prénom>/churn »

**À observer** : le modèle bat le modèle de référence, mais sans miracle. Sur une liste de même taille que celle
de la règle, la précision progresse à peine : ces clients inactifs, la règle les trouve déjà. Où le modèle gagne-t-il vraiment ?
(indice : chez les clients achetés récemment, que la règle des 270 jours ne cible jamais). Quel rôle jouent
les ouvertures d'e-mails ? Lisez `VALIDATION.md` : ses dix rubriques sont celles de la fiche de la slide.

## Étape 6 - Le biais de l'anonymisation (10 min, en autonomie)

> « Les clients inactifs depuis deux ans sont anonymisés (vérifie dans la fiche de la table clients et dans les données à qui la règle s'applique vraiment) : identité effacée, historique détaché, et s'ils reviennent ils reçoivent un nouvel identifiant. Mesure l'ampleur du phénomène dans les données (clients anonymisés, commandes sans client par année) et explique comment il fausse la photo churn et le taux de perte observé. Que faudrait-il demander à l'équipe données pour corriger ce biais ? »

## Étape 7 - La liste de ciblage d'aujourd'hui (15 min, en autonomie)

Pour une vraie campagne, on ne cible pas des clients au 30/06/2025 : on cible les clients d'aujourd'hui
(dans le kit, le 31/12/2025, date d'extraction). On entraîne sur la dernière photo dont la cible est connue,
et on note la photo du jour.

> « Réentraîne le modèle, avec les mêmes variables, sur la photo du 30 juin 2025 (sa cible est connue). Construis la photo du 31 décembre 2025 avec les mêmes définitions de colonnes, sans cible. Note-la avec le modèle, puis produis la liste de ciblage pour la campagne de relance : les 1 000 clients les plus à risque parmi ceux qui sont inscrits aux e-mails et qui ont acheté il y a moins de 270 jours au 31/12/2025, avec leur identifiant, leur probabilité, et la raison principale en quelques mots. Enregistre-la dans travail/<prénom>/churn/ciblage.csv, avec une note sur la façon de mesurer l'effet de la campagne (groupe témoin). »

## Comment vérifier

- L'auditeur a nommé la colonne fautive, avec une preuve chiffrée.
- Sans cette colonne, les résultats sont nettement moins bons qu'à l'étape 3 (où presque tout était juste).
- Liste de même taille que la règle (environ 2 990 clients) : précision d'environ 92 % pour les deux.
- Parmi les 1 000 clients récents (moins de 270 jours) les plus à risque : 730 à 745 vrais perdus pour le modèle
  (selon les variables retenues), environ 690 en les classant par ancienneté du dernier achat, environ 380 au hasard.
- `VALIDATION.md` compare le modèle et la règle sur la même population et le même test, et cite le biais d'anonymisation dans les limites.
- `ciblage.csv` contient 1 000 lignes, aucun client anonymisé, aucun client hors de la population demandée,
  et les récences sont calculées au 31/12/2025.

## Pour aller plus loin

- Industrialisez le modèle dans `projets/churn/` avec des tests, et ajoutez une page « Ciblage des clients à risque »
  au portail (le portail l'annonce déjà comme « à venir »).
- `/expliquer travail/<prénom>/churn` pour préparer une présentation au marketing.
- Construisez six photos mensuelles de 2024 (fin janvier à fin juin), entraînez sur leur réunion et testez sur
  la photo du 30/06/2025. Comment traiter un client présent sur plusieurs photos ?
- Préparez lundi : `lundi/ml-bigquery.md` donne la photo en SQL BigQuery, `CREATE MODEL`, `ML.EVALUATE` et
  `ML.PREDICT`, et `lundi/a-demander.md` un modèle de demande au DPO pour figer une photo par mois.
- Comparez la liste du modèle à celle de la règle : combien de clients en commun ?
