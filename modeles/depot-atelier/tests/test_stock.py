from fastapi.testclient import TestClient

from app import stock
from app.main import app

client = TestClient(app)


def test_lecture_du_stock():
    lignes = stock.lire_stock()
    assert len(lignes) == 13
    assert all(isinstance(l["stock"], int) for l in lignes)


def test_alertes_triees_du_stock_le_plus_bas():
    valeurs = [l["stock"] for l in stock.alertes()]
    assert valeurs == sorted(valeurs)
    assert valeurs[0] == 0


def test_page_accueil():
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert "Pull col rond mérinos" in reponse.text


def test_api_alertes():
    reponse = client.get("/api/alertes")
    assert reponse.status_code == 200
    assert {l["boutique"] for l in reponse.json()} <= {"Lille", "Lyon", "Nantes", "Paris"}
