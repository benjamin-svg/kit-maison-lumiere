"""Stock des boutiques : application d'atelier.

Lancement : uv run uvicorn app.main:app --reload, puis ouvrir http://127.0.0.1:8000
"""

from html import escape

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app import stock

app = FastAPI(title="Stock des boutiques")


@app.get("/", response_class=HTMLResponse)
def accueil() -> str:
    lignes = "".join(
        f"<tr><td>{escape(l['boutique'])}</td><td>{escape(l['reference'])}</td><td>{escape(l['article'])}</td>"
        f"<td>{l['stock']}</td><td>{l['seuil_alerte']}</td></tr>"
        for l in stock.alertes()
    )
    return (
        "<!doctype html><html lang='fr'><meta charset='utf-8'><title>Stock des boutiques</title>"
        "<h1>Articles à réapprovisionner</h1>"
        "<table><tr><th>Boutique</th><th>Référence</th><th>Article</th><th>Stock</th><th>Seuil</th></tr>"
        f"{lignes}</table></html>"
    )


@app.get("/api/stock")
def api_stock() -> list[dict]:
    return stock.lire_stock()


@app.get("/api/alertes")
def api_alertes() -> list[dict]:
    return stock.alertes()
