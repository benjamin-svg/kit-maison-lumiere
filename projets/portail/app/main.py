"""Portail intranet de Maison Lumière (application de formation).

Lancement, depuis projets/portail/ :
    uv run uvicorn app.main:app --reload
puis ouvrir http://127.0.0.1:8000
"""

from datetime import date
from html import escape

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from app import commandes, delais
from app.applications import APPLICATIONS
from app.gabarit import page, tableau

app = FastAPI(title="Portail Maison Lumière")


@app.get("/", response_class=HTMLResponse)
def accueil() -> str:
    cartes = []
    for a in APPLICATIONS:
        nom = f'<a href="{a["lien"]}">{escape(a["nom"])}</a>' if a["lien"] else escape(a["nom"])
        cartes.append(
            f'<div class="carte"><strong>{nom}</strong> <span class="statut">({escape(a["statut"])})</span>'
            f'<br>{escape(a["description"])}</div>'
        )
    return page("Applications", "".join(cartes))


@app.get("/api/applications")
def api_applications() -> list[dict]:
    return APPLICATIONS


@app.get("/delais-fournisseurs", response_class=HTMLResponse)
def page_delais(pays: str | None = Query(default=None)) -> str:
    lignes = delais.lire_delais(pays)
    options = "".join(
        f'<option value="{escape(p)}"{" selected" if pays and p.lower() == pays.lower() else ""}>{escape(p)}</option>'
        for p in delais.liste_pays()
    )
    formulaire = (
        '<form method="get"><label>Pays : <select name="pays"><option value="">Tous</option>'
        f"{options}</select></label> <button type=\"submit\">Filtrer</button></form>"
    )
    tab = tableau(
        ["Fournisseur", "Pays", "Famille", "Délai moyen (j)", "Délai max (j)", "Retards (%)", "Mise à jour"],
        [[l["fournisseur"], l["pays"], l["famille"], l["delai_moyen_jours"], l["delai_max_jours"],
          l["taux_retard_pct"], l["derniere_maj"]] for l in lignes],
        numeriques={3, 4, 5},
    )
    intro = "<p>Fournisseurs classés du délai moyen le plus long au plus court.</p>"
    pied = (f"<p>{len(lignes)} fournisseur(s)</p>"
            f"<p>Délai moyen des fournisseurs affichés : {delais.delai_moyen(lignes)} j</p>")
    return page("Délais fournisseurs", intro + formulaire + tab + pied)


@app.get("/api/delais-fournisseurs")
def api_delais(pays: str | None = Query(default=None)) -> list[dict]:
    return delais.lire_delais(pays)


@app.get("/commandes-du-jour", response_class=HTMLResponse)
def page_commandes(jour: date | None = Query(default=None, alias="date")) -> str:
    if not commandes.chemin_base().exists():
        return page("Suivi des commandes du jour",
                    "<p>La base n'existe pas. Lancez : <code>uv run python donnees/generer_donnees.py</code></p>")
    jour = jour or commandes.derniere_date()
    lignes = commandes.commandes_du_jour(jour)
    formulaire = (f'<form method="get"><label>Date : <input type="date" name="date" value="{jour}"></label> '
                  '<button type="submit">Afficher</button></form>')
    if not lignes:
        return page("Suivi des commandes du jour", formulaire + f"<p>Aucune commande le {jour}.</p>")
    tab = tableau(
        ["Canal", "Commandes", "Articles", "CA net HT (€)"],
        [[l["canal"], l["nb_commandes"], l["nb_articles"], f'{l["ca_net_ht"]:,.2f}'.replace(",", " ")]
         for l in lignes],
        numeriques={1, 2, 3},
    )
    return page("Suivi des commandes du jour",
                formulaire + f"<p>Commandes du {jour} (commandes annulées exclues).</p>" + tab)


@app.get("/api/commandes-du-jour")
def api_commandes(jour: date | None = Query(default=None, alias="date")) -> dict:
    jour = jour or commandes.derniere_date()
    return {"date": str(jour), "canaux": commandes.commandes_du_jour(jour)}
