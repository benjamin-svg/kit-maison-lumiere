# Portail intranet Maison Lumière (projet d'exercice)

Petite application web FastAPI qui sert de terrain pour les exercices « software factory ».
Les données sont fictives.

## Structure

- `app/main.py` : les routes (pages HTML et API JSON).
- `app/applications.py` : la liste des applications affichées sur l'accueil.
- `app/delais.py` : lecture de `donnees/delais_fournisseurs.csv` (page « Délais fournisseurs »).
- `app/commandes.py` : lecture de la base DuckDB du kit (page « Suivi des commandes du jour »).
- `app/gabarit.py` : gabarit HTML commun.
- `conftest.py` : fixtures pytest, dont une petite base DuckDB de test (indépendante des données générées).
- `tests/` : tests automatisés.
- `tickets/` : les demandes à traiter (évolutions et retours de recette).

## Commandes (à lancer depuis `projets/portail/`)

- Tests : `uv run pytest -q`
- Lancer le portail : `uv run uvicorn app.main:app --reload` puis ouvrir http://127.0.0.1:8000
- La page des commandes lit `../../donnees/ecommerce.duckdb` (variable `PORTAIL_BASE` pour en changer).

## Règles pour ce projet

- Une demande = un ticket de `tickets/` = une branche git `ticket/T-xxx-mot-cle`.
- Avant de corriger une anomalie, écrire d'abord un test qui la reproduit et vérifier qu'il échoue.
- Ne jamais modifier un test existant pour le faire passer : si un test existant semble faux, le signaler.
- Garder le code simple : pas de nouvelle dépendance, pas de moteur de gabarits, HTML via `app/gabarit.py`.
- Les calculs de CA suivent `semantique/metriques.yml` à la racine du kit (commandes annulées exclues).
- Après chaque modification, les tests sont relancés automatiquement par un hook : lire leur résultat.
- Les messages de commit sont en français, au présent : « Ajoute le filtre famille (T-101) ».
