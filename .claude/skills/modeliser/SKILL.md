---
name: modeliser
description: Conduit un projet de modélisation (prévision ou classification, par exemple churn) de bout en bout selon les pratiques du métier - partir de la décision et du coût des erreurs, définir la cible en dates, battre une règle simple, valider sur le futur, mesurer l'incertitude, industrialiser et surveiller. À utiliser quand on démarre un modèle de machine learning sur les données de formation.
argument-hint: "[objectif du modèle]"
---

# Modéliser, étape par étape

Objectif : $ARGUMENTS

Travailler dans `travail/<prénom>/` pour l'exploration, puis dans `projets/<nom-du-projet>/` pour la version
industrialisée (tests compris). Demander le prénom s'il n'est pas connu.

Cette skill suit les pratiques reconnues du métier : partir de la décision (démarche CRISP-DM), commencer
par une règle simple et un modèle simple (« Rules of Machine Learning » de Google), valider sur des données
postérieures et par backtest (Hyndman et Athanasopoulos, « Forecasting: Principles and Practice »),
traquer les fuites (Kapoor et Narayanan), documenter avant la mise en service (« Model Cards »).

## 1. Cadrer (en mode plan, sans écrire de code)

Proposer un plan et attendre l'accord avant de coder. Le plan répond à :

- **Décision et action** : qui utilisera le résultat, pour faire quoi, à quelle fréquence, avec quelle
  capacité (par exemple : 1 000 clients relancés par mois ; des intérimaires réservés deux semaines avant).
- **Coût des erreurs** : que coûte une erreur dans chaque sens ? (prévoir trop : du personnel payé à
  attendre ; prévoir trop peu : des retards. Cibler un client fidèle : une remise donnée pour rien ;
  rater un client sur le départ : une vente perdue.) Ce coût choisit la mesure de réussite.
- **Cible** : que prédit-on exactement ? Bornes écrites en dates, pas en nombre de jours (« aucune commande
  non annulée du 01/07/2025 au 31/12/2025 inclus » ; « commandes web non annulées de la semaine du lundi
  au dimanche »). Une cible doit être close avant la date de la photo de test.
- **Fenêtres temporelles** : date de référence, fenêtre d'observation (le passé que l'on regarde),
  fenêtre de la cible (le futur), horizon de prévision. Faire un petit schéma texte.
- **Données disponibles le jour de la prédiction** : seulement ce qui est connu ce jour-là. Une table
  « état du jour » (statut, dernière date, inscription aux e-mails) ne dit pas ce qu'on savait avant ;
  un plan commercial a des versions (`plan_commercial`) ; une commande peut être annulée ou retournée après coup.
- **Calendrier** : semaines ISO ou décalage de 364 jours ? Que faire d'une semaine 53 (2026 en a une) ?
- **Mesure de réussite**, lisible par le métier et liée à la décision : erreur moyenne en commandes, WAPE,
  biais ; part des clients perdus retrouvés dans une liste de la taille prévue (précision à N).
- **Données personnelles** (churn) : quelles données sur des personnes, pour quel usage, et faut-il en parler
  au DPO (délégué à la protection des données) ? Respecter les désinscriptions aux e-mails.

## 2. Regarder les données avant de modéliser

Courbe de la série ou répartition de la cible ; volumes par période ; valeurs vides ; ruptures (nouveau
canal, changement de définition) ; événements exceptionnels. Écrire ce qu'on en retient avant de choisir
une méthode.

## 3. Poser la règle simple à battre

Avant tout modèle, calculer une référence simple et compréhensible :
- prévision : « même semaine l'an dernier », ou « moyenne des 4 dernières semaines » ;
- churn : « perdu si pas d'achat depuis 270 jours », et le simple classement par ancienneté du dernier achat.
Mesurer cette règle avec la même mesure et sur la même période de test que le futur modèle.
Si le modèle ne bat pas nettement la règle, garder la règle : elle est plus simple à expliquer et à maintenir.

## 4. Construire

- Préparer les données avec des requêtes ou un script relisibles ; contrôler les lignes et les doublons.
  Chaque variable est calculée « à la date » (avec ce qui était connu ce jour-là).
- Commencer par un modèle simple (régression logistique, lissage exponentiel), puis seulement ensuite
  plus complexe si le gain le justifie.
- Découpage **temporel** : entraîner sur le passé, tester sur une période ultérieure. Pour une prévision,
  backtest à origine glissante (on se place à chaque date passée et on prévoit avec ce qui était connu).
- Toute préparation qui apprend des données (moyennes, normalisation, choix de variables, réglages) se fait
  sur la seule période d'apprentissage.
- Choisir la méthode sur une période, et donner son score sur une **autre** période : sinon le score est
  trop optimiste (on a choisi la méthode qui a eu de la chance sur ces semaines-là).
- **Incertitude** : pour une prévision, donner une fourchette (par exemple les erreurs passées au 10e et au
  90e centile) et vérifier sur le backtest qu'environ 80 % des semaines y tombent. Pour un score de churn
  utilisé comme une probabilité, vérifier qu'il est calibré (sur 100 clients notés 0,30, environ 30 partent).
- **Analyse des erreurs** : où le modèle se trompe-t-il le plus (semaines d'opérations, petits clients,
  région) ? Le dire.
- **Reproductibilité** : graine fixée, versions des bibliothèques, date des données, paramètres notés.

## 5. Valider

- Utiliser la skill `valider-modele` pour produire `VALIDATION.md`.
- Faire appel au sous-agent `auditeur-fuite` avant de conclure, surtout si le résultat paraît trop beau.

## 6. Industrialiser et surveiller

- Créer `projets/<nom>/` avec un code organisé (préparation, entraînement, prédiction), un `README.md`,
  et des tests pytest (le hook les relance à chaque modification d'un fichier Python).
- Un script qui tourne sans Claude (par exemple `prevoir_hebdo.py --date-origine AAAA-MM-JJ`), qui **ajoute**
  une version datée de la prévision (ou des scores) dans un fichier ou une table, sans écraser les précédentes,
  avec la version du code et du modèle.
- Une **surveillance** : comparer chaque semaine (ou chaque mois) la prévision au réel ; une règle d'alerte
  écrite (par exemple erreur des 4 dernières semaines supérieure à 1,5 fois celle du backtest) ; qui reçoit
  l'alerte, et le retour à la règle simple si le modèle se dégrade.
- Pour une campagne (churn) : un **groupe témoin** tiré au hasard dans la liste, qui ne reçoit pas l'offre,
  pour mesurer ce que la campagne rapporte. Un bon score de départ ne prouve pas que la relance fait revenir.
- Si demandé : une petite API FastAPI et une interface Streamlit qui lisent le modèle enregistré.
- Utiliser la skill `expliquer` pour produire `EXPLICATION.md`.

## Règles

- Annoncer à chaque étape ce qui a été contrôlé.
- Ne jamais modifier `donnees/brutes/`. Ne pas lire `exercices/` ni `donnees/generer_donnees.py`.
