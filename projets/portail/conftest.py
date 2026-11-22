"""Fixtures communes : une petite base DuckDB de test, indépendante des données générées."""

from datetime import date

import duckdb
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def base_test(tmp_path, monkeypatch):
    chemin = tmp_path / "test.duckdb"
    con = duckdb.connect(str(chemin))
    con.execute("""CREATE TABLE commandes (id_commande BIGINT, id_client BIGINT, date_commande DATE,
                   canal VARCHAR, statut VARCHAR)""")
    con.execute("""CREATE TABLE lignes_commande (id_ligne BIGINT, id_commande BIGINT, id_produit BIGINT,
                   quantite INT, prix_unitaire_ht DOUBLE, remise_ht DOUBLE, montant_ht DOUBLE,
                   quantite_retournee INT, montant_retourne_ht DOUBLE)""")
    con.execute("""INSERT INTO commandes VALUES
        (1, 10, '2025-12-30', 'WEB', 'LIVREE'),
        (2, 11, '2025-12-30', 'WEB', 'ANNULEE'),
        (3, 12, '2025-12-30', 'MAGASIN', 'LIVREE'),
        (4, 13, '2025-12-31', 'WEB', 'EN_COURS')""")
    con.execute("""INSERT INTO lignes_commande VALUES
        (1, 1, 1001, 1, 50.0, 0.0, 50.0, 0, 0.0),
        (2, 1, 1002, 2, 20.0, 0.0, 40.0, 1, 20.0),
        (3, 2, 1003, 1, 99.0, 0.0, 99.0, 0, 0.0),
        (4, 3, 1001, 1, 50.0, 5.0, 45.0, 0, 0.0),
        (5, 4, 1004, 1, 30.0, 0.0, 30.0, 0, 0.0)""")
    con.close()
    monkeypatch.setenv("PORTAIL_BASE", str(chemin))
    return chemin


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


@pytest.fixture
def jour_test():
    return date(2025, 12, 30)
