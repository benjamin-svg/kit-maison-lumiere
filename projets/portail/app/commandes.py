"""Lecture des commandes du jour dans la base DuckDB de la formation."""

import os
from datetime import date
from pathlib import Path

import duckdb

RACINE_KIT = Path(__file__).resolve().parents[3]
BASE_PAR_DEFAUT = RACINE_KIT / "donnees" / "ecommerce.duckdb"


def chemin_base() -> Path:
    return Path(os.environ.get("PORTAIL_BASE", BASE_PAR_DEFAUT))


def connexion() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(chemin_base()), read_only=True)


def derniere_date() -> date | None:
    with connexion() as con:
        return con.execute("SELECT MAX(date_commande) FROM commandes").fetchone()[0]


def commandes_du_jour(jour: date) -> list[dict]:
    """Une ligne par canal : commandes non annulées, articles et CA net HT (retours déduits)."""
    sql = """
        SELECT c.canal,
               COUNT(DISTINCT c.id_commande) AS nb_commandes,
               SUM(l.quantite) AS nb_articles,
               ROUND(SUM(l.montant_ht - l.montant_retourne_ht), 2) AS ca_net_ht
        FROM commandes c
        JOIN lignes_commande l ON l.id_commande = c.id_commande
        WHERE c.date_commande = ? AND c.statut <> 'ANNULEE'
        GROUP BY c.canal
        ORDER BY c.canal
    """
    with connexion() as con:
        lignes = con.execute(sql, [jour]).fetchall()
    return [
        {"canal": canal, "nb_commandes": int(nb), "nb_articles": int(art), "ca_net_ht": float(ca)}
        for canal, nb, art, ca in lignes
    ]
