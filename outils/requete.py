"""Exécute une requête SQL en lecture seule sur la base DuckDB de la formation.

Exemples :
    uv run python outils/requete.py "SELECT COUNT(*) FROM commandes"
    uv run python outils/requete.py -f travail/celine/analyses/ca_web.sql
    uv run python outils/requete.py "SELECT * FROM produits" --limite 10
    uv run python outils/requete.py -f requete.sql --csv travail/celine/analyses/resultat.csv
    uv run python outils/requete.py --tables          (liste les tables et leurs colonnes)

La connexion est ouverte en lecture seule : aucune requête ne peut modifier la base.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "donnees" / "ecommerce.duckdb"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sql", nargs="?", help="requête SQL entre guillemets")
    parser.add_argument("-f", "--fichier", help="fichier .sql à exécuter")
    parser.add_argument("--limite", type=int, default=50, help="nombre de lignes affichées (50 par défaut)")
    parser.add_argument("--csv", help="enregistre le résultat complet dans ce fichier CSV")
    parser.add_argument("--tables", action="store_true", help="liste les tables et leurs colonnes")
    args = parser.parse_args()

    if not BASE.exists():
        print("La base n'existe pas encore. Lancez d'abord : uv run python donnees/generer_donnees.py")
        return 1
    con = duckdb.connect(str(BASE), read_only=True)

    if args.tables:
        df = con.execute(
            "SELECT table_name AS table, column_name AS colonne, data_type AS type "
            "FROM information_schema.columns WHERE table_schema = 'main' ORDER BY table_name, ordinal_position"
        ).df()
        for table, groupe in df.groupby("table", sort=False):
            n = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f"\n{table} ({n} lignes)")
            for r in groupe.itertuples():
                print(f"  - {r.colonne} : {r.type}")
        return 0

    if args.fichier:
        sql = Path(args.fichier).read_text(encoding="utf-8")
    elif args.sql:
        sql = args.sql
    else:
        parser.print_help()
        return 1

    try:
        df = con.execute(sql).df()
    except duckdb.Error as e:
        print(f"Erreur SQL : {e}")
        return 1

    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 30)
    print(df.head(args.limite).to_string(index=False))
    print(f"\n{len(df)} ligne(s) au total" + (f", {args.limite} affichée(s)" if len(df) > args.limite else ""))
    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.csv, index=False)
        print(f"Résultat enregistré dans {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
