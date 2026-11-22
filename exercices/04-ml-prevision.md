# Exercice 04 - Prévoir les commandes web de la semaine

## Objectif

Construire avec Claude une prévision hebdomadaire du nombre de commandes web, à 1 semaine et à 12 semaines,
en suivant une méthode rigoureuse : cadrage, règle simple à battre (« même semaine l'an dernier »),
test sur le passé (« backtest »), **choix de la méthode sur une période et note sur une autre**, validation,
puis industrialisation : un script qui tourne chaque lundi sans Claude et garde chaque version de la prévision,
une API (FastAPI) et une interface (Streamlit).
Refaire l'exercice sur la série des articles encombrants, plus petite et plus bruitée.

## Durée

90 minutes.

## Vocabulaire

- **Origine** : le lundi où l'on fait la prévision. On n'utilise que ce qu'on savait ce jour-là, donc les commandes
  jusqu'au dimanche de la veille.
- **Horizon** : combien de semaines à l'avance on prévoit. **Horizon 1** : la semaine qui commence le lundi de
  l'origine (on prévoit la semaine en cours avec les données jusqu'à la veille). **Horizon 12** : la semaine qui
  commence 11 semaines plus tard.
- **Fourchette (intervalle de prévision)** : les bornes basse et haute entre lesquelles le réel devrait tomber,
  par exemple 8 fois sur 10. On la tire des erreurs du backtest, horizon par horizon. C'est elle qui dit
  quand croire le chiffre : une prévision de 400 commandes « entre 340 et 470 » ne se lit pas comme « entre 390 et 410 ».
- **Backtest** : on se replace à une date passée, on prévoit avec les seules données connues à cette date,
  et on compare au réel. On répète sur plusieurs dates.
- **Naïve saisonnière** : la prévision « même semaine l'an dernier ». Simple, et souvent difficile à battre.
- **MAE** : erreur moyenne, en commandes. **MAPE** : erreur moyenne en pourcentage du réel, semaine par semaine.
  **WAPE** : erreur totale divisée par le réel total ; plus stable que la MAPE quand certaines semaines sont
  petites (encombrants). **Biais** : le modèle prévoit-il en moyenne trop ou pas assez ?

## Étape 1 - Cadrer en mode plan (15 min)

Passez en mode plan (Maj+Tab), puis :

> « /modeliser Prévision hebdomadaire du nombre de commandes web non annulées, à 1 semaine et à 12 semaines, pour dimensionner la logistique. »

**À observer** : Claude propose la cible exacte, la définition de la semaine (du lundi au dimanche ?),
les fenêtres, la règle simple, la mesure d'erreur, la période de test. Discutez au moins :
- que faire des semaines incomplètes au début et à la fin des données ?
- quelle table utiliser (`commandes` ou `commandes_jour`) ? Que dit `semantique/` ?
- les opérations commerciales tombent-elles à la même semaine chaque année ? Que savait-on du plan le jour
  de la prévision ? (`plan_commercial` garde chaque version du plan, `calendrier_commercial` les dates réalisées)
- 2026 a une **semaine 53** (du 28/12/2026 au 03/01/2027) : une prévision à 12 semaines lancée en octobre la
  traverse. « Même semaine l'an dernier » : décalage de 364 jours, ou même numéro de semaine ISO ?
- une commande peut être annulée après coup : le nombre de la dernière semaine connue peut encore baisser.

Validez le plan quand il vous convient, puis sortez du mode plan.

## Étape 2 - La série et la règle simple (15 min)

> « Construis la série hebdomadaire des commandes web non annulées dans travail/<prénom>/prevision/, avec les contrôles habituels, et trace-la avec matplotlib dans un fichier PNG. Puis fais un backtest de la prévision "même semaine l'an dernier", à 1 semaine et à 12 semaines, sur la période de choix seulement (les 26 premières semaines de 2025, du 30/12/2024 au 23/06/2025). Ne calcule rien encore sur la période de note (les 26 suivantes, du 30/06/2025 au 22/12/2025) : on la garde pour la fin. Donne MAE, MAPE, WAPE et biais. »

**À observer** : le nombre de semaines, les semaines incomplètes écartées, le pic du Black Friday,
le creux d'août, la tendance. Pour la naïve saisonnière, l'erreur est la même aux deux horizons : pourquoi ?

## Étape 3 - Battre la règle simple, sans tricher sur le choix (20 min)

> « Propose deux méthodes un peu plus élaborées (par exemple la même semaine l'an dernier corrigée de la tendance récente, et une méthode qui tient compte des opérations du plan commercial dans sa version connue le jour de la prévision). Fais exactement le même backtest sur la période de choix, et choisis la meilleure méthode pour chaque horizon. Ensuite seulement, donne le score de la règle simple et de la méthode choisie sur la période de note. Présente un tableau : période, méthode, horizon, MAE, MAPE, WAPE, biais. »

**À observer** :
- Claude n'utilise que des informations connues à la date de la prévision : les commandes futures, non ;
  le plan commercial, oui, mais **dans la version publiée avant l'origine** (une vente privée a été déplacée
  d'une semaine en septembre 2025).
- Pourquoi deux périodes ? Si l'on choisit la méthode sur les semaines qui servent à la noter, on prend celle
  qui a eu de la chance sur ces semaines-là, et sa note est trop belle.
- Quelles semaines restent mal prévues ? (indice : ventes privées et opérations « livraison offerte »
  qui changent de date d'une année sur l'autre).
- Une méthode qui fait mieux à 12 semaines qu'à 1 semaine n'a pas forcément une fuite : sur 26 semaines,
  le hasard compte. Faites vérifier par le sous-agent `auditeur-fuite` avant de conclure.

## Étape 4 - La série des encombrants (10 min)

> « Refais les étapes 2 et 3 sur le nombre hebdomadaire d'articles encombrants vendus sur le web (mobilier, tapis, mobilier enfant). Compare les erreurs (WAPE) avec celles de la série des commandes et explique la différence. La méthode choisie sur la période de choix est-elle encore la meilleure sur la période de note ? »

**À observer** : une série de 30 à 40 articles par semaine est beaucoup plus bruitée ; l'erreur en
pourcentage est plus forte, et la méthode gagnante change d'une période à l'autre. Conclusion possible :
garder la règle simple pour les encombrants, ou prévoir au mois.

## Étape 5 - Valider (10 min)

> « /valider-modele travail/<prénom>/prevision »

**À observer** : `VALIDATION.md` compare la méthode et la règle simple sur au moins deux périodes, pour
chaque série. Si la méthode ne bat pas la règle sur une série, l'avis doit le dire : c'est un résultat utile.

## Étape 6 - Industrialiser (20 min)

> « Industrialise dans projets/prevision/ la méthode retenue pour chaque série : un module de prévision ; un script prevoir_hebdo.py --date-origine AAAA-MM-JJ qui calcule les prévisions de 1 à 12 semaines avec les seules données connues à cette date et les ajoute, datées, à projets/prevision/sorties/previsions.csv sans effacer les précédentes ; une règle d'alerte qui signale quand l'erreur moyenne des 4 dernières semaines dépasse 1,5 fois l'erreur moyenne du backtest sur la période de note, pour la même série et le même horizon ; une API FastAPI avec une route /prevision?serie=web&horizon=12 ; une interface Streamlit qui affiche la série et la prévision ; un README et des tests pytest (dont un test de l'API et un test qui vérifie qu'une deuxième exécution ajoute des lignes sans effacer les premières). Lance les tests, puis dis-moi les commandes pour lancer le script, l'API et l'interface. »

Lancez le script pour deux lundis différents, puis l'interface (`uv run streamlit run projets/prevision/<fichier>.py`)
et l'API (`uv run uvicorn ...`).

**À observer** : à chaque fichier Python modifié sous `projets/prevision/`, le hook relance les tests.
Le script est ce qui tournera chaque lundi dans un pipeline GitLab planifié, sans Claude (voir `lundi/gitlab.md`).
L'API et l'interface servent à consulter le résultat.

## Comment vérifier

- Le tableau du backtest contient la règle simple et au moins deux méthodes, aux deux horizons, sur les deux périodes.
- Règle simple, commandes web, période de choix : MAPE **13,6 %** environ (étape 2).
- Règle simple, commandes web, période de note : MAPE **15,4 %** (à quelques dixièmes près selon la définition des semaines).
- `cd projets/prevision && uv run pytest -q` : tous les tests passent.
- `projets/prevision/sorties/previsions.csv` contient deux dates d'origine différentes.
- `VALIDATION.md` donne un avis par série, sur au moins deux périodes de test.

## Pour aller plus loin

- `/expliquer projets/prevision` : lisez `EXPLICATION.md` et répondez aux trois questions de contrôle.
- Ajoutez une fourchette (intervalle de prévision à 80 %, tirée des erreurs du backtest, par horizon) et affichez-la
  dans Streamlit. Puis vérifiez sur la période de note : le réel tombe-t-il dedans 8 fois sur 10 ?
- Préparez lundi : lisez `lundi/ml-bigquery.md` et demandez à Claude de traduire votre requête de série
  hebdomadaire en SQL BigQuery (semaines ISO), puis d'écrire le `CREATE MODEL` ARIMA_PLUS_XREG qui servirait
  de méthode concurrente.
