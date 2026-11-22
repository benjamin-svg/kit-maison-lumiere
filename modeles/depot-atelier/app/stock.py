"""Lecture du stock des boutiques et repérage des articles à réapprovisionner."""

import csv
import os
from pathlib import Path

CHEMIN_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "donnees" / "stock.csv"


def chemin_fichier() -> Path:
    return Path(os.environ.get("STOCK_CSV", CHEMIN_PAR_DEFAUT))


def lire_stock() -> list[dict]:
    """Toutes les lignes du fichier, avec stock et seuil convertis en entiers."""
    with open(chemin_fichier(), encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    for l in lignes:
        l["stock"] = int(l["stock"])
        l["seuil_alerte"] = int(l["seuil_alerte"])
    return lignes


def a_reapprovisionner(ligne: dict) -> bool:
    """Un article est à réapprovisionner quand son stock passe sous le seuil d'alerte."""
    return ligne["stock"] < ligne["seuil_alerte"]


def alertes() -> list[dict]:
    """Les articles à réapprovisionner, du stock le plus bas au plus haut."""
    return sorted((l for l in lire_stock() if a_reapprovisionner(l)), key=lambda l: l["stock"])
