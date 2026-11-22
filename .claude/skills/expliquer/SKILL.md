---
name: expliquer
description: Explique un code ou un projet à quelqu'un qui ne l'a pas écrit - rôle de chaque fichier, choix et hypothèses, trajet d'une dizaine de lignes de données, ce qui casserait, trois questions de contrôle - et écrit EXPLICATION.md. À utiliser pour comprendre ou transmettre un code produit avec Claude.
argument-hint: "[dossier ou fichier]"
---

# Expliquer un code

Cible : $ARGUMENTS (si rien n'est indiqué, demander quel dossier ou fichier).

Écrire pour une personne qui connaît le métier mais pas forcément Python ni SQL. Phrases courtes,
termes techniques expliqués la première fois.

Aller du général au détail : d'abord à quoi sert le code et ce qu'il produit, en deux phrases ; ensuite
les pièces ; enfin un exemple réel suivi de bout en bout. Une explication se vérifie : finir par des questions.

## Plan de l'explication

0. **En deux phrases** : à quoi sert ce code, qui l'utilise, ce qu'il produit.
1. **Rôle de chaque fichier** : un tableau fichier | rôle en une phrase | qui l'appelle.
2. **Choix et hypothèses** : les décisions prises (définitions, filtres, paramètres, seuils), pourquoi,
   et ce qui se passerait avec un autre choix.
3. **Trajet de 10 lignes** : prendre 10 lignes réelles de données en entrée (les extraire vraiment,
   en lecture seule) et montrer ce qu'elles deviennent à chaque étape, jusqu'au résultat final.
4. **Ce qui casserait** : 3 à 5 changements plausibles qui casseraient le code ou fausseraient le résultat
   sans erreur visible (colonne renommée, nouvelle valeur de statut, données manquantes, changement de période...),
   et comment on s'en apercevrait.
5. **Mots techniques** : les termes utilisés, chacun défini en une phrase avec un exemple tiré du code.
6. **Trois questions de contrôle** : trois questions (avec leurs réponses à la fin) pour vérifier
   qu'on a compris.

## Étapes

- Lire le code, l'exécuter si c'est rapide et sans risque, extraire les 10 lignes.
- Écrire `EXPLICATION.md` à côté du code expliqué (ou dans `travail/<prénom>/` si le dossier n'est pas à soi).
- Résumer en trois lignes et poser à la personne la première question de contrôle.
