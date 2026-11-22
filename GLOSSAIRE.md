# Glossaire du kit

Les mots techniques des slides, des fiches et des réponses de Claude, avec un exemple pris dans le kit.
Le support donne le mot français d'abord, puis entre parenthèses le mot que vous lirez à l'écran
(dans Claude Code, GitLab ou un article). Ce glossaire donne les deux.
Un mot manque ? Demandez à Claude : « Explique-moi <mot> en deux phrases, avec un exemple du kit. »

## Claude Code

| Mot | Ce que c'est | Exemple |
|---|---|---|
| Agent | Un programme qui enchaîne lui-même lecture, action et vérification pour atteindre un but | Claude lit `semantique/`, écrit la requête, la lance, contrôle le total |
| Contexte | Tout ce que Claude a sous les yeux dans la session : consignes, fichiers lus, échanges | `CLAUDE.md` est dans le contexte dès le démarrage |
| Compacter | Résumer automatiquement une longue conversation pour libérer de la place dans le contexte | Après une heure de travail, Claude garde un résumé au lieu de tout l'historique |
| `CLAUDE.md` | Le fichier de consignes lu à chaque session | La règle « ne jamais modifier `donnees/brutes/` » |
| Mode plan | Mode où Claude lit et propose un plan sans rien modifier (Maj+Tab) | Le plan de la page « 10 produits les plus vendus » |
| Procédure (skill) | Un fichier de consignes pour une tâche, appelé par `/nom` | `/analyse`, `.claude/skills/analyse/SKILL.md` |
| Sous-agent | Un Claude séparé, avec son propre contexte, pour une tâche précise | Le `verificateur` recalcule un chiffre sans voir la première requête |
| Déclencheur (hook) | Un programme lancé par Claude Code avant ou après une action, qui peut la refuser | `garde_fou.py` refuse `rm -rf` |
| PreToolUse, PostToolUse | Les moments où un hook est lancé : avant une action (pour refuser), après (pour réagir) | Avant : garde-fou. Après : relancer les tests |
| Code 2 | Le code de sortie par lequel un hook signale un problème à Claude | Le hook de tests renvoie 2 quand un test échoue |
| Matcher | La liste des outils qui déclenchent un hook | `"Bash\|Write\|Edit"` |
| `settings.json` | Le fichier de réglages : permissions et hooks | `.claude/settings.json` |
| Permissions `allow`, `ask`, `deny` | Ce que Claude peut faire sans demander, en demandant, ou jamais | `deny` : lire `exercices/` |
| Classifieur | En mode Auto, le contrôle qui juge si une action est assez sûre pour être lancée sans vous demander | Une suppression massive est arrêtée et vous est soumise |
| `bypassPermissions`, `dontAsk` | Des modes où Claude ne demande plus l'autorisation : à éviter sur un vrai projet | - |
| Connecteur (serveur MCP) | Un connecteur qui donne à Claude des outils vers un service | Un serveur MCP BigQuery qui lance des requêtes |
| Extension (plugin) | Un paquet qui regroupe skills, sous-agents, hooks et serveurs MCP, à installer d'un coup | Les outils de l'équipe partagés en un seul plugin |
| `claude -p` | Claude Code lancé sans conversation, pour une seule consigne (dans un script) | `claude -p "résume ce fichier"` |
| `/rewind` | Revenir à un point antérieur de la conversation, et annuler les modifications de fichiers de Claude | Effacer `essai.md` créé par erreur |
| Diff (vue des différences) | L'affichage des lignes ajoutées et retirées d'un fichier | La vue de Desktop avant d'accepter une modification |
| Worktree | Une deuxième copie de travail du même dépôt git, sur une autre branche, pour travailler en parallèle | Deux tickets traités en même temps dans deux dossiers |

## Git et GitLab

| Mot | Ce que c'est | Exemple |
|---|---|---|
| Dépôt | Le dossier suivi par git, avec tout son historique | Le kit |
| Version (commit) | Une photo enregistrée des fichiers, avec un message qui dit pourquoi | « Ajoute le filtre famille (T-101) » |
| Branche | Une ligne de travail parallèle | `ticket/T-101-filtre-famille` |
| HEAD | Le commit sur lequel on se trouve | Après `git switch main`, HEAD est le dernier commit de `main` |
| Fusion (merge) | Ramener le travail d'une branche dans une autre | T-103 fusionnée dans `main` |
| Conflit | Deux branches ont modifié la même ligne ; un humain choisit | Le point 3 de l'ordre du jour |
| Envoyer, récupérer (push, pull) | Envoyer ses commits au serveur, récupérer ceux des autres | `git push -u origin ticket/A-201` |
| Demande de fusion (merge request, MR) | Sur GitLab, la demande de fusionner une branche, avec diff, tests et relecture | `glab mr create` |
| Chaîne de contrôles (pipeline, CI) | Les vérifications lancées automatiquement à chaque modification, décrites dans `.gitlab-ci.yml` | Les tests du portail à chaque merge request |
| Tâche (job) | Une tâche d'un pipeline | Le job `tests` |
| Exécutant (runner) | La machine qui exécute les jobs | Un runner partagé de l'entreprise |
| Dépôt distant (remote, origin) | La copie du dépôt sur le serveur, vers laquelle on envoie ses versions | `origin`, le dépôt sur GitLab |
| Pull request (PR) | Le nom de la demande de fusion sur GitHub | Les articles sur Stripe ou Spotify parlent de PR |
| Branche protégée | Une branche où personne ne pousse directement | `main` |
| `glab` | L'outil de GitLab en ligne de commande | `glab mr view 3 --comments` |
| `Closes #4` | Écrit dans une merge request, ferme le ticket 4 à la fusion | - |

## Usine logicielle (software factory)

| Mot | Ce que c'est | Exemple |
|---|---|---|
| Usine logicielle (software factory) | La chaîne outillée qui mène un ticket jusqu'à la mise en production, avec des contrôles à chaque étape | Ticket, branche, tests, relecture, merge request |
| Recette | La vérification par le métier que la livraison fait ce qui était demandé | Le ticket T-103 de l'acheteuse |
| Critère d'acceptation | Une condition vérifiable qu'une livraison doit remplir | « `famille=pull` renvoie 4 fournisseurs » |
| Test (pytest) | Un petit programme qui vérifie un comportement et échoue s'il change | `test_filtre_pays` |
| Fixture | Des données ou un objet préparés pour les tests | La petite base DuckDB de `conftest.py` |
| Linter | Un outil qui repère les erreurs de forme dans le code | Ruff pour Python |
| Refactoriser | Réorganiser le code sans changer ce qu'il fait | Renommer une fonction et ses appels |
| « Étant donné... quand... alors » | Une façon d'écrire un critère : situation, action, résultat attendu | Étant donné le filtre Portugal, quand j'ouvre la page, alors je vois 12,6 j |
| `SPEC.md` | Un fichier qui décrit ce qu'il faut construire, écrit avant le code | La spécification d'une nouvelle page |
| Webhook | Un appel envoyé automatiquement par un service quand un événement se produit | GitLab prévient un autre outil à chaque merge request |
| FastAPI, uvicorn | Une bibliothèque pour écrire une application web en Python, et le programme qui la fait tourner | Le portail |
| Streamlit | Une bibliothèque pour faire une interface web simple en Python | L'interface de la prévision |
| API | Une adresse qui renvoie des données à un programme, pas à une personne | `/api/delais-fournisseurs` |

## Données et couche sémantique

| Mot | Ce que c'est | Exemple |
|---|---|---|
| Couche sémantique | Ce qui dit ce que veulent dire les données : rôle des tables, grain, jointures, définitions des indicateurs | `semantique/` |
| Grain | Ce que représente une ligne d'une table | `lignes_commande` : un produit dans une commande |
| Agrégat | Une table de totaux précalculés | `commandes_jour` |
| Jointure | Relier deux tables par une colonne commune | `commandes` et `lignes_commande` sur `id_commande` |
| Doublon après jointure | Une valeur répétée sur plusieurs lignes après une jointure, puis additionnée à tort | `montant_ttc` répété sur chaque ligne de commande |
| Métrique | Un indicateur avec une définition unique | `ca_net_ht` |
| Dimension, mesure | Ce par quoi on découpe (canal, mois), ce qu'on additionne (CA, commandes) | CA (mesure) par canal (dimension) |
| Entité | Un objet métier qu'on décrit | Le client, la commande |
| YAML | Un format de fichier texte pour des données structurées, lisible par une personne | `metriques.yml` |
| Markdown | Un format de texte simple avec titres et tableaux | Les fiches de `semantique/tables/` |
| DuckDB | Une base de données qui tient dans un fichier, sur le poste | `donnees/ecommerce.duckdb` |
| BigQuery | L'entrepôt de données de Google Cloud, facturé au volume lu | Les vraies données, lundi |
| Partition | Le découpage d'une table (souvent par date) qui permet de ne lire qu'une partie | Filtrer la date fait lire moins |
| Dry run | L'estimation, gratuite, du volume qu'une requête lirait | `bq query --dry_run` |
| dbt, Dataform, MetricFlow, Cube, Looker | Des outils qui gèrent une couche sémantique ou des transformations SQL | Pour plus tard, si `semantique/` ne suffit plus |
| CTE (`WITH ... AS`) | Une sous-requête nommée, en tête de requête, pour découper un calcul | `WITH ventes AS (...) SELECT ...` |
| `COALESCE`, `NULLIF` | Remplacer une valeur vide ; rendre vide une valeur (pour éviter une division par zéro) | `NULLIF(nb_commandes, 0)` |
| `FILTER (WHERE ...)` | Un total avec une condition, dans DuckDB (`COUNTIF` dans BigQuery) | Compter les annulées |
| Date de rattachement | La date qui décide à quel jour ou quel mois on compte une ligne | Une commande passée le 30/11 et livrée le 03/12 compte en novembre si l'on rattache à la date de commande |
| Statut `BROUILLON`, `VALIDEE` | L'état d'une définition : en cours d'écriture, ou relue et acceptée par son propriétaire | Seule une métrique `VALIDEE` sert à un chiffre diffusé |
| Point de pourcentage | L'écart entre deux pourcentages, à ne pas confondre avec une variation en % | De 20 % à 25 % : +5 points, soit +25 % |
| Médiane | La valeur du milieu : la moitié est au-dessous, la moitié au-dessus | Moins sensible qu'une moyenne aux très gros paniers |
| Paramètre (`:date_obs`) | Une case à remplir dans une formule | La date d'observation des clients actifs |
| Opt-in | L'accord du client pour recevoir des e-mails | `optin_email` |
| Haché | Remplacé par un code qui ne permet pas de retrouver la valeur | `email_hash` |
| Anonymisation | Effacement de l'identité d'un client inactif | Dans le kit : après 2 ans sans commande, avec des exceptions à trouver dans les données |
| UTC | L'heure de référence mondiale, une à deux heures de moins que Paris | Une commande à 0 h 30 à Paris est la veille en UTC |
| Graine fixe | Le point de départ du hasard d'un programme : même graine, mêmes données | `GRAINE = 20251231` |
| `uv` | L'outil qui installe Python et les bibliothèques du kit | `uv sync` |

## Méthode ML

| Mot | Ce que c'est | Exemple |
|---|---|---|
| Départs de clients (churn) | Les clients qui cessent d'acheter | Un client sans commande dans les 6 mois après la photo |
| Cible | Ce que le modèle prédit | `perdu_6m` |
| Règle simple | La méthode évidente que le modèle doit battre | « Pas d'achat depuis 270 jours » |
| Photo (à une date) | Les clients tels qu'ils étaient à une date, avec la cible observée après | `clients_churn_snapshot` au 30/06/2025 |
| Fuite de données | Une information inconnue le jour de la prédiction, utilisée par le modèle | Prévoir les ventes d'une opération avec le plan commercial dans sa version finale, publiée après coup |
| Test sur le passé (backtest) | Se replacer dans le passé, prévoir, comparer au réel, et recommencer | 26 semaines de 2025 |
| Origine | La date où l'on fait la prévision ; on n'utilise que ce qu'on savait ce jour-là | Le lundi 30/06/2025, avec les commandes jusqu'au dimanche 29/06 |
| Fourchette (intervalle de prévision) | Les bornes entre lesquelles le réel devrait tomber, par exemple 8 fois sur 10 | « 400 commandes, entre 340 et 470 » |
| Horizon | Combien de temps à l'avance on prévoit | 1 semaine, 12 semaines |
| MAE, MAPE, WAPE | Erreur moyenne ; erreur moyenne en % ; erreur totale divisée par le réel total | MAPE de 15,4 % pour la règle simple |
| Biais | Le modèle prévoit-il en moyenne trop, ou pas assez ? | -49,9 commandes par semaine |
| Précision, rappel | Parmi les ciblés, combien partent ; parmi les partants, combien sont ciblés | 91,9 % et 50,3 % pour la règle |
| AUC | La probabilité qu'un partant soit classé au-dessus d'un fidèle (0,5 = hasard, 1 = parfait) | 0,853 |
| Régression logistique | Un modèle simple qui pondère les variables pour donner une probabilité | Le modèle churn du kit |
| Sur-apprentissage | Un modèle qui colle au passé et se trompe sur des données nouvelles | Les annales apprises par cœur |
| Groupe témoin | Des clients tirés au hasard qui ne reçoivent pas l'offre, pour mesurer son effet | 10 % de la liste de relance |
| Semaine ISO, semaine 53 | Semaines du lundi au dimanche, numérotées ; certaines années en ont 53 | 2026 |
