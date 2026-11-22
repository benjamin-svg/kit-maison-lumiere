---
name: valider-modele
description: Produit le fichier VALIDATION.md d'un modèle selon les pratiques de validation du métier (fiche de type Model Card) - décision, cible, données, variables connues à la date, découpage temporel, règle simple contre modèle sur plusieurs périodes, incertitude, stabilité, cas vérifiés à la main, limites, surveillance et responsables. À utiliser quand un modèle (prévision, churn) est construit et qu'il faut décider si on peut s'en servir.
argument-hint: "[dossier du modèle]"
---

# Valider un modèle

Dossier du modèle : $ARGUMENTS (si rien n'est indiqué, demander lequel).

La fiche s'inspire des « Model Cards » (Mitchell et al., 2019) et des fiches contre les fuites de Kapoor et
Narayanan. Son but : qu'une personne qui n'a pas construit le modèle puisse décider de s'en servir, ou non,
en connaissant ses limites.

## Étapes

1. Lire le code du modèle et ses résultats. Identifier la décision servie, la cible, les variables,
   la date de référence, le découpage entraînement/test.
2. **Recalculer** les mesures (ne pas recopier des chiffres affichés plus tôt) :
   - la mesure principale du modèle sur la période de test ;
   - la même mesure pour la règle simple (prévision : « même semaine l'an dernier » ; churn : « pas d'achat
     depuis 270 jours » et classement par ancienneté du dernier achat) sur exactement la même période et la
     même population ;
   - pour un classement de clients : la précision et le rappel à N égal pour la règle et pour le modèle
     (N = la taille de la liste prévue), et l'AUC ;
   - pour une prévision : MAE, MAPE, WAPE (erreur absolue totale divisée par le réel total) et biais, par horizon.
3. **Contrôles** à faire et à noter :
   - aucune variable connue après la date de référence (faire appel au sous-agent `auditeur-fuite`) ;
   - découpage temporel, pas aléatoire ; méthode choisie sur une période et notée sur une autre ;
   - stabilité : résultat sur au moins deux périodes de test différentes, et par segment (canal, région,
     ancienneté) ;
   - incertitude : fourchette de prévision et part des semaines qui y tombent ; pour un score utilisé comme
     probabilité, calibration (taux réel de départ par tranche de score) ;
   - populations absentes ou biaisées (clients anonymisés, identifiants vides) ;
   - reproductibilité : relancer l'entraînement redonne-t-il les mêmes chiffres ?
4. **Vérifier dix cas à la main** : prendre dix lignes (clients ou semaines) au hasard, recalculer leurs variables
   et leur cible directement depuis les tables de base, et comparer.
5. Écrire `VALIDATION.md` dans le dossier du modèle. Le plan suit les dix questions de la fiche de validation
   (slide « Avant la mise en service, une fiche d'une page répond à dix questions ») :

```markdown
# Validation : <nom du modèle>
## 1. Décision, utilisateur, fréquence (et coût d'une erreur dans chaque sens)
## 2. Cible ou série, horizons (bornes en dates)
## 3. Données, période, population, traitement de l'anonymisation (tables, nombre de lignes, date des données)
## 4. Variables : connue à la date de référence ? (variable | date de calcul | oui/non | preuve)
## 5. Découpage temporel (période d'apprentissage, période de choix, période de test, écart entre elles)
## 6. Règle simple contre modèle, par période de test (tableau : période | mesure | règle simple | modèle | écart),
##    avec l'incertitude (fourchette et taux de couverture, ou calibration)
## 7. Stabilité (par période et par segment) et 5 variables principales
## 8. Dix cas vérifiés à la main (cas | valeur recalculée | valeur du modèle | identique ?)
## 9. Limites et usages interdits (dont données personnelles et avis du DPO si besoin)
## 10. Responsables, surveillance et date de revue (responsable métier, responsable technique ; règle d'alerte,
##     qui la reçoit, retour à la règle simple ; date de la prochaine revue)
## Avis : utilisable / utilisable avec réserves / pas utilisable, et pourquoi
```

   Si une rubrique ne peut pas être remplie (par exemple les responsables), écrire « À COMPLÉTER » et le dire.
6. Résumer l'avis en trois lignes à la personne. Proposer qu'une autre personne relise la fiche avant la
   mise en service : celui qui a construit le modèle n'est pas le mieux placé pour en voir les failles.

## Règles

- Si le modèle ne bat pas la règle simple, le dire clairement : c'est un résultat utile.
- Ne pas lire `exercices/` ni `donnees/generer_donnees.py`.
