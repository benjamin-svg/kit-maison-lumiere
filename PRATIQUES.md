# Sur quelles pratiques reposent les outils du kit

Les skills, les sous-agents et les formats du kit ne sont pas des recettes propres à Claude Code. Chacun
reprend les pratiques reconnues de son métier ; Claude Code sert seulement à les appliquer à chaque fois.
Lundi, si vous adaptez un outil, gardez ces pratiques : ce sont elles qui rendent le résultat fiable.

## Analyse de données (`/analyse`, `verificateur`, `analyse-bigquery`)

| Pratique | Où dans le kit |
|---|---|
| Partir de la décision : qui demande, pour décider quoi | `/analyse`, étape 1 |
| Définir l'indicateur avant de calculer, avec une définition validée | `/analyse` étape 1, `semantique/metriques.yml` |
| Comparer à périmètre égal : même durée, décalage de 364 jours, même périmètre | `/analyse`, étape 3 |
| Décomposer un écart (commandes × panier, par canal) ; donner les effectifs à côté des taux | `/analyse`, étape 3 |
| Contrôler : lignes, doublons après jointure, total recoupé, ordre de grandeur | `/analyse`, étape 5 |
| Ne pas confondre un constat et une cause : un effet se mesure contre un témoin | `/analyse`, étape 6 |
| Contrôle à quatre yeux : un second analyste recalcule seul | sous-agent `verificateur` |
| La réponse d'abord, puis l'explication, puis les limites ; une note qui permet de refaire le calcul | `/analyse`, étape 7 |

## Documentation des données (`/documenter-table`, `semantique/`)

| Pratique | Où dans le kit |
|---|---|
| Une seule définition par indicateur, avec un propriétaire | `metriques.yml`, champs `definition`, `proprietaire` |
| Le grain d'une table, prouvé par une requête | fiche de table, section 2 |
| Origine, fréquence de mise à jour, historique ou état du jour | fiche de table, section 1 |
| Données personnelles signalées | fiche de table, section 5 |
| Des contrôles qu'on relance à chaque mise à jour (clé unique, jamais vide, jointures complètes) | fiche de table, section 8 |
| Une formule exécutable et un exemple qui sert de test | `metriques.yml`, champs `formule_sql`, `exemple` |
| Dire si un indicateur s'additionne (un panier moyen ne s'additionne pas) | `metriques.yml`, champ `additivite` |
| Une définition se relit comme du code avant d'être validée | `semantique/README.md`, sous-agent `relecteur` |

## Méthode ML (`/modeliser`, `/valider-modele`, `auditeur-fuite`)

| Pratique | Source | Où dans le kit |
|---|---|---|
| Partir de la décision et du coût des erreurs | démarche CRISP-DM | `/modeliser`, étape 1 |
| Une règle simple d'abord, un modèle simple ensuite | Google, « Rules of Machine Learning » | `/modeliser`, étapes 3 et 4 |
| Valider sur le futur, par backtest à origine glissante | Hyndman et Athanasopoulos, « Forecasting: Principles and Practice » | `/modeliser`, étape 4 |
| Choisir la méthode sur une période, la noter sur une autre | même source | `/modeliser`, `/valider-modele` |
| Donner une fourchette de prévision ; vérifier qu'un score est calibré | même source ; scikit-learn | `/modeliser`, étape 4 |
| Traquer les fuites (variables connues après coup, préparation apprise sur le test...) | Kapoor et Narayanan, 2023 ; scikit-learn, « Common pitfalls » | sous-agent `auditeur-fuite` |
| Une fiche de validation avant la mise en service, relue par une autre personne | Mitchell et al., « Model Cards », 2019 | `/valider-modele` |
| Surveiller, et revenir à la règle simple si le modèle se dégrade | Google, « Rules of Machine Learning » | `/modeliser`, étape 6 |
| Mesurer l'effet d'une campagne avec un groupe témoin | pratique du test contrôlé | `/modeliser`, étape 6 |

## Développement (`/ticket-vers-merge-request`, `/recette`, `relecteur`, hooks)

| Pratique | Où dans le kit |
|---|---|
| Un ticket prêt : des critères vérifiables (« étant donné, quand, alors ») | `/ticket-vers-merge-request`, étape 1 |
| Une demande = une branche ; le plus petit changement, sans hors-sujet | étapes 2 et 3 |
| Test d'abord : écrire le test, le voir échouer, puis coder | étape 4 ; `/recette`, étape 3 |
| Les tests relancés à chaque modification, comme une intégration continue | hook `lancer_tests.py` ; `.gitlab-ci.yml` lundi |
| Petits commits, messages clairs avec l'identifiant du ticket | étape 6 |
| Relire son propre diff, puis une relecture par un autre | étape 7 ; sous-agent `relecteur` (grille inspirée du guide de relecture de Google) |
| Ne jamais affaiblir un test pour obtenir du vert | `CLAUDE.md` du projet ; `relecteur`, point 4 |
| Corriger la cause, pas le symptôme ; chercher le même défaut ailleurs | `/recette`, étapes 4 et 7 |
| Ne jamais insérer un texte de l'utilisateur dans du HTML ou du SQL sans l'échapper | étape 4 ; `relecteur`, point 6 |
| La fusion est décidée par un humain, après un pipeline vert | étape 10 ; réglages GitLab de `modeles/factory/` |
| Des garde-fous automatiques pour les gestes dangereux | hook `garde_fou.py` |
