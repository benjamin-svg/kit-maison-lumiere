"""Lecture du fichier des délais fournisseurs."""

import csv
import os
from pathlib import Path

CHEMIN_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "donnees" / "delais_fournisseurs.csv"


def chemin_fichier() -> Path:
    return Path(os.environ.get("PORTAIL_DELAIS_CSV", CHEMIN_PAR_DEFAUT))


def lire_delais(pays: str | None = None) -> list[dict]:
    """Renvoie les fournisseurs, du délai moyen le plus long au plus court.

    pays : si renseigné, ne garde que les fournisseurs de ce pays.
    """
    with open(chemin_fichier(), encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    if pays:
        lignes = [l for l in lignes if l["pays"].lower() == pays.lower()]
    return sorted(lignes, key=lambda l: l["delai_moyen_jours"], reverse=True)


def delai_moyen(lignes: list[dict]) -> int:
    """Délai moyen, en jours, des fournisseurs donnés (0 si la liste est vide)."""
    if not lignes:
        return 0
    total = sum(int(l["delai_moyen_jours"]) for l in lignes)
    return total // len(lignes)


def liste_pays() -> list[str]:
    with open(chemin_fichier(), encoding="utf-8", newline="") as f:
        return sorted({l["pays"] for l in csv.DictReader(f)})
