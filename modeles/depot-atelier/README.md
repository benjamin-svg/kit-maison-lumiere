# Stock des boutiques (dépôt d'atelier)

Petite application web qui affiche le stock de chaque article dans chaque boutique de Maison Lumière,
et signale les ruptures. Données fictives.

Ce dépôt sert à l'exercice 07 du kit : **il ne contient volontairement aucune configuration Claude Code**
(ni `CLAUDE.md`, ni `.claude/`). C'est à vous de monter la chaîne « ticket, branche, tests, relecture,
merge request ».

## Commandes

```bash
uv sync                                  # installe les dépendances (une fois)
uv run pytest                            # lance les tests
uv run uvicorn app.main:app --reload     # lance l'application : http://127.0.0.1:8000
```

## Organisation

- `app/main.py` : les routes (page HTML et API JSON).
- `app/stock.py` : lecture de `donnees/stock.csv` et calcul des ruptures.
- `tests/` : tests automatisés (pytest).
- `tickets/` : les demandes à traiter.
