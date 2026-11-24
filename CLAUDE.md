# Kit de formation Claude Code - Maison Lumière

## Contexte

Ce dossier est un kit de formation. Les participants font partie de l'équipe e-commerce d'une marque
de prêt-à-porter, appelée ici **Maison Lumière** (nom fictif). **Toutes les données sont fictives** :
elles sont générées par `donnees/generer_donnees.py` avec une graine fixe. Aucune donnée réelle, aucun
accès à BigQuery ni à GitLab : tout tourne en local (DuckDB, Python, git).

Participants : Maxime (chef de projet technique), Céline (analyste, débute en SQL), Olivier (prévision
des commandes web), Augustin (churn, c'est-à-dire la perte de clients). Si tu ne connais pas le prénom
de la personne, demande-le une fois au début : il sert à choisir son dossier `travail/<prénom>/`.

## Structure du dépôt

- `donnees/generer_donnees.py` : génère la base et les CSV.
- `donnees/ecommerce.duckdb` : la base DuckDB (générée, non versionnée).
- `donnees/brutes/` : les mêmes tables en CSV (générées, non versionnées). **Lecture seule.**
- `semantique/` : la couche sémantique (fiches des tables, définitions des métriques). À lire avant tout SQL.
- `outils/requete.py` : exécute une requête SQL en lecture seule sur la base.
- `outils/tester_hooks.py` : vérifie que les garde-fous fonctionnent.
- `outils/depot_distant.py` et `outils/simuler_collegue.py` : le dépôt distant simulé de la démonstration 3
  (il joue le rôle de GitLab) et un collègue qui y fusionne une correction.
- `projets/portail/` : petite application web d'intranet (FastAPI) pour la démonstration et les exercices sur l'usine logicielle.
- `projets/` : les projets industrialisés (un dossier par projet, avec ses tests).
- `demos/` : le parcours rapide, 5 démonstrations, une par partie de la formation. Tu peux les lire.
- `exercices/` : les exercices complets, de `00` à `08`, au choix avec le parcours rapide. **Elles sont pour le participant, pas pour toi** :
  ne les lis pas (un hook le refuse). Le participant te donne la consigne.
- `travail/<prénom>/` : l'espace de travail de chaque participant (analyses, brouillons, modèles).
  Non versionné, sauf `travail/<prénom>/git/` (démonstration 2 et exercice 01).
- `modeles/` : des points de départ à copier hors du kit (dépôt d'atelier, usine logicielle, BigQuery).
- `lundi/` : les fiches pour refaire le travail sur les vraies données (BigQuery, GitLab).
- `GLOSSAIRE.md` : les mots techniques du kit, expliqués avec un exemple.
- `.claude/` : réglages, hooks (garde-fous), sous-agents et skills du kit.

Tables de la base : `produits`, `clients`, `commandes`, `lignes_commande`, `emails`,
`calendrier_commercial`, `plan_commercial`, `commandes_jour`, `clients_churn_snapshot`.

## Règles

1. **Ne jamais modifier `donnees/brutes/`** (ni à la main, ni par script). Pour transformer des données,
   écrire le résultat dans `travail/<prénom>/`. Un hook refuse ces écritures.
2. **Travailler dans `travail/<prénom>/`** pour tout ce qui est personnel (analyses, essais, notes).
   Les projets destinés à durer vont dans `projets/<nom>/`, avec des tests.
3. **Toujours lire `semantique/` avant d'écrire du SQL** : `semantique/README.md`, `semantique/metriques.yml`
   et les fiches des tables utilisées. Utiliser les définitions validées ; si une fiche ou une métrique est
   `A_COMPLETER`, le dire et demander comment trancher.
4. **Toujours annoncer les contrôles faits** : nombre de lignes, doublons après jointure, valeurs vides,
   total comparé à une référence. Un chiffre sans contrôle annoncé n'est pas fini.
5. **Expliquer en français simple** : phrases courtes, termes techniques expliqués la première fois,
   pas d'anglicismes inutiles. **Tutoyer** la personne, du début à la fin de la session.
6. **Pas de suppression récursive** (`rm -rf` est refusé par un hook). Supprimer fichier par fichier.
7. **Ne pas lire `exercices/` ni `donnees/generer_donnees.py`** : les fiches sont pour le participant, et le
   script de génération n'existe pas sur les vraies données. Documenter les tables à partir des données.
   Le lancer (`uv run python donnees/generer_donnees.py`) reste permis.
8. Avant une tâche de plus de quelques minutes, proposer un plan et attendre l'accord.
9. **Les définitions des métriques vivent dans `semantique/` seulement.** Ne pas les recopier dans ce fichier
   (même si `/init` le propose) : deux copies d'une définition finissent par se contredire.

## Commandes utiles

- Installer : `uv sync`
- Générer les données (moins d'une minute) : `uv run python donnees/generer_donnees.py`
- Lister les tables et colonnes : `uv run python outils/requete.py --tables`
- Requête SQL en lecture seule : `uv run python outils/requete.py "SELECT ..."`
  (ou `-f fichier.sql`, `--csv sortie.csv`, `--limite 100`)
- Tests du portail : `cd projets/portail && uv run pytest -q`
- Lancer le portail : `cd projets/portail && uv run uvicorn app.main:app --reload` (http://127.0.0.1:8000)
- Lancer une interface Streamlit : `uv run streamlit run <fichier.py>`
- Vérifier les garde-fous : `uv run python outils/tester_hooks.py`

## Outils du kit dans `.claude/`

- Skills (commandes `/nom`) : `/documenter-table`, `/analyse`, `/entrainer-modele` (une phrase devient un
  script qui entraîne un modèle), `/modeliser`, `/valider-modele`,
  `/expliquer`, `/recette`, `/ticket-vers-merge-request`, et le cycle d'un ticket :
  `/start-dev` (branche et worktree dans `.worktrees/<ticket>/`), `/sync-dev` (mise à jour avec le dépôt
  distant), `/close-dev` (tests, relecture, merge request, sans fusion).
- Règles par sujet (`.claude/rules/`) : `sql.md`, lue seulement quand un fichier `.sql` est ouvert.
- Sous-agents : `verificateur` (recalcule un chiffre par un autre chemin), `auditeur-fuite` (cherche
  les fuites de données dans un modèle), `relecteur` (relit une branche comme une merge request).
- Hooks : refus des écritures dans `donnees/brutes/`, de `rm -rf` et de la lecture de `exercices/` ;
  tests relancés automatiquement quand un fichier Python de `projets/` change. Quand le participant te
  demande explicitement d'essayer une action pour voir le refus du hook, fais une vraie tentative avec
  l'outil normal (pas une simulation) : le hook bloquera, c'est le but de la démonstration. Si l'action
  passe quand même, le hook n'est pas chargé : arrête-toi, dis-le, et remets le fichier dans son état
  (pour `donnees/brutes/`, relancer `uv run python donnees/generer_donnees.py`).

## Repères sur les données

- Commandes du 1er janvier 2023 au 31 décembre 2025 ; canaux `WEB`, `MAGASIN`, `MARKETPLACE`.
- Montants : `lignes_commande` est en euros HT ; `commandes.montant_ttc` est TTC, frais de port compris.
- Date de référence de la photo churn (`clients_churn_snapshot`) : 30 juin 2025.
- `calendrier_commercial` donne les dates **réalisées** des opérations ; `plan_commercial` donne le plan
  **tel qu'il était connu** à chaque date de publication (une ligne par version), plan 2026 compris.
