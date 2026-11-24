"""Tableau des tickets du kit, qui joue le rôle du tableau de Jira (ou de GitLab).

Dans Jira, chaque ticket est rangé dans une colonne : À faire, En cours, En relecture, Terminé.
Le kit n'a ni Jira ni GitLab : ce script tient le tableau dans `.depot-distant/tableau-tickets.md`,
à côté du dépôt distant simulé. Il liste tous les tickets de `projets/*/tickets/`.

Usage (depuis le dossier du kit ou un worktree) :
    uv run python outils/tableau.py                      # affiche le tableau
    uv run python outils/tableau.py T-101 "En cours"     # range le ticket T-101 dans une colonne

Colonnes : « À faire », « En cours », « En relecture », « Terminé ».
Dans Jira, la même action se fait sur la page du ticket. Les skills du cycle la font ici :
/start-dev (En cours), /ship-dev (En relecture), /close-dev (Terminé).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

COLONNES = ["À faire", "En cours", "En relecture", "Terminé"]


def racine_du_kit() -> Path:
    """Dossier principal du kit, même si l'on est dans un worktree."""
    ici = Path(__file__).resolve().parent
    r = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       cwd=ici, capture_output=True, text=True, check=True)
    return Path(r.stdout.strip()).parent


def tickets(racine: Path) -> dict[str, str]:
    """{identifiant: titre} pour chaque fichier projets/*/tickets/T-xxx-*.md."""
    res = {}
    for f in sorted(racine.glob("projets/*/tickets/T-*.md")):
        ident = re.match(r"(T-\d+)", f.name).group(1)
        premiere = f.read_text(encoding="utf-8").splitlines()[0]
        titre = re.sub(r"^#\s*T-\d+\s*:\s*", "", premiere).strip()
        res[ident] = titre
    return res


def lire(chemin: Path) -> dict[str, str]:
    """{identifiant: colonne} lu dans le fichier du tableau."""
    etat, colonne = {}, None
    if chemin.exists():
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("## "):
                colonne = ligne[3:].strip()
            m = re.match(r"- (T-\d+)", ligne)
            if m and colonne in COLONNES:
                etat[m.group(1)] = colonne
    return etat


def ecrire(chemin: Path, etat: dict[str, str], titres: dict[str, str]) -> None:
    lignes = ["# Tableau des tickets (joue le rôle du tableau de Jira)", ""]
    for c in COLONNES:
        lignes.append(f"## {c}")
        for ident in sorted((i for i in titres if etat.get(i, "À faire") == c), key=lambda i: int(i[2:])):
            lignes.append(f"- {ident} : {titres[ident]}")
        lignes.append("")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(lignes), encoding="utf-8")


def main() -> None:
    racine = racine_du_kit()
    chemin = racine / ".depot-distant" / "tableau-tickets.md"
    titres = tickets(racine)
    etat = lire(chemin)
    if len(sys.argv) == 3:
        ident, colonne = sys.argv[1].upper(), sys.argv[2]
        if ident not in titres:
            sys.exit(f"Ticket inconnu : {ident}. Tickets : {', '.join(titres)}")
        if colonne not in COLONNES:
            sys.exit(f"Colonne inconnue : {colonne}. Colonnes : {', '.join(COLONNES)}")
        avant = etat.get(ident, "À faire")
        etat[ident] = colonne
        ecrire(chemin, etat, titres)
        print(f"{ident} : {avant} → {colonne}")
    elif len(sys.argv) == 1:
        ecrire(chemin, etat, titres)
    else:
        sys.exit(__doc__)
    print(chemin.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
