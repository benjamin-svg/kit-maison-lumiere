"""Merge requests du kit, qui jouent le rôle de celles de GitLab.

Le kit n'a pas de vrai GitLab. Chaque merge request est un fichier
`.depot-distant/merge-requests/<identifiant>.md`, à côté du dépôt distant simulé : tout le monde la voit
au même endroit, et elle ne disparaît pas avec le worktree. Les skills du cycle la tiennent à jour :

    /start-dev  ouvre la merge request en brouillon, dès que la branche est envoyée ;
    /sync-dev   met à jour sa description à chaque envoi ;
    /ship-dev   termine la description et la passe « Prête à relire » ;
    la personne qui relit la fusionne (le bouton « Merge » de GitLab) : commande `fusionner` ;
    /close-dev  fait le ménage sur le poste.

Usage (depuis le dossier du kit ou un worktree) :
    uv run python outils/merge_request.py                               # liste les merge requests
    uv run python outils/merge_request.py ouvrir T-101 <branche> "<titre>"
    uv run python outils/merge_request.py prete T-101                   # retire le statut brouillon
    uv run python outils/merge_request.py fusionner T-101               # le bouton « Merge »

`fusionner` est réservé à la personne qui relit : elle le tape elle-même, précédé de « ! » dans Claude Code.
Comme GitLab, il refuse une merge request en brouillon, et une branche en conflit avec main
(il faut alors lancer /sync-dev sur la branche). Il fusionne sur le dépôt distant, sans toucher aux dossiers
de travail, puis supprime la branche sur le dépôt distant (la case « Delete source branch » de GitLab).

Sur un vrai GitLab : `glab mr create --draft`, `glab mr update <n> --description`, `glab mr update <n> --ready`,
et le bouton « Merge » de la page de la merge request.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depot_distant import chemin_distant, est_le_distant_simule, racine_du_kit, url_origin  # noqa: E402

BROUILLON, PRETE, FUSIONNEE = "Brouillon", "Prête à relire", "Fusionnée"


def git(*args: str, cwd: Path, verifier: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if verifier and r.returncode != 0:
        sys.exit(f"Erreur : git {' '.join(args)}\n{r.stderr.strip()}")
    return r


def dossier_mr(racine: Path) -> Path:
    return racine / ".depot-distant" / "merge-requests"


def lire_champ(texte: str, champ: str) -> str | None:
    m = re.search(rf"^- {champ} : (.*)$", texte, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def changer_champ(texte: str, champ: str, valeur: str) -> str:
    return re.sub(rf"^- {champ} : .*$", f"- {champ} : {valeur}", texte, count=1, flags=re.MULTILINE)


def fichier_ticket(racine: Path, ident: str) -> Path:
    trouves = sorted(racine.glob(f"projets/*/tickets/{ident}-*.md"))
    if not trouves:
        sys.exit(f"Ticket inconnu : {ident} (aucun fichier projets/*/tickets/{ident}-*.md).")
    return trouves[0]


def criteres(ticket: Path) -> list[str]:
    """Les critères d'acceptation numérotés du ticket, une ligne chacun."""
    texte = ticket.read_text(encoding="utf-8")
    partie = texte.split("## Critères d'acceptation", 1)[-1].split("\n## ", 1)[0]
    res, courant = [], None
    for ligne in partie.splitlines():
        m = re.match(r"\s*(\d+)\.\s+(.*)", ligne)
        if m:
            courant = [m.group(2).strip()]
            res.append(courant)
        elif courant is not None and ligne.strip():
            courant.append(ligne.strip())
    return [" ".join(c) for c in res]


def verifier_distant(racine: Path) -> Path:
    if not est_le_distant_simule(url_origin(racine), racine):
        sys.exit("Ce kit n'utilise pas le dépôt distant simulé. Sur un vrai GitLab, utilisez glab ou la page "
                 "de la merge request. Pour préparer le dépôt simulé : uv run python outils/depot_distant.py")
    return chemin_distant(racine)


def lister(racine: Path) -> None:
    fichiers = sorted(dossier_mr(racine).glob("T-*.md"), key=lambda f: int(f.stem[2:]))
    if not fichiers:
        print("Aucune merge request pour l'instant (/start-dev en ouvre une pour chaque ticket).")
        return
    for f in fichiers:
        texte = f.read_text(encoding="utf-8")
        titre = texte.splitlines()[0].lstrip("# ").strip()
        print(f"{f.stem} [{lire_champ(texte, 'Statut')}] {titre} : {f.relative_to(racine)}")


def ouvrir(racine: Path, ident: str, branche: str, titre: str) -> None:
    distant = verifier_distant(racine)
    chemin = dossier_mr(racine) / f"{ident}.md"
    if chemin.exists():
        print(f"La merge request de {ident} existe déjà ({lire_champ(chemin.read_text(encoding='utf-8'), 'Statut')}) :"
              f" {chemin.relative_to(racine)}")
        return
    if not git("rev-parse", "--verify", "--quiet", f"refs/heads/{branche}", cwd=distant, verifier=False).stdout:
        sys.exit(f"La branche {branche} n'est pas sur le dépôt distant. L'envoyer d'abord : git push -u origin {branche}")
    ticket = fichier_ticket(racine, ident)
    titre = re.sub(rf"\s*\(?{ident}\)?\s*$", "", titre.strip())  # l'identifiant est ajouté ici, une seule fois
    lignes = [f"# {titre} ({ident})", "",
              f"- Branche : {branche} → main",
              f"- Statut : {BROUILLON}",
              f"- Ticket : {ticket.relative_to(racine)}",
              f"- Ouverte le : {dt.date.today():%d/%m/%Y}", "",
              "## Ce qui change", "", "(rien pour l'instant : /sync-dev complète cette partie à chaque envoi)", "",
              "## Critères du ticket", "",
              "| Critère | Test qui le prouve (fichier et nom du test) | Résultat |", "|---|---|---|"]
    lignes += [f"| {i}. {c} | à écrire | à faire |" for i, c in enumerate(criteres(ticket), 1)]
    lignes += ["", "## Tests", "", "(pas encore lancés)", "",
               "## Relecture du sous-agent", "", "(faite par /ship-dev)", "",
               "## Comment tester", "", "(complété par /ship-dev)", "",
               "## Risques et retour arrière", "", "(complété par /ship-dev)", ""]
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    print(f"Merge request ouverte en brouillon : {chemin.relative_to(racine)}")


def prete(racine: Path, ident: str) -> None:
    chemin = dossier_mr(racine) / f"{ident}.md"
    if not chemin.exists():
        sys.exit(f"Pas de merge request pour {ident}. /start-dev l'ouvre.")
    texte = chemin.read_text(encoding="utf-8")
    statut = lire_champ(texte, "Statut")
    if statut == FUSIONNEE:
        sys.exit(f"La merge request de {ident} est déjà fusionnée.")
    chemin.write_text(changer_champ(texte, "Statut", PRETE), encoding="utf-8")
    print(f"{ident} : {statut} → {PRETE}")


def fusionner(racine: Path, ident: str) -> None:
    distant = verifier_distant(racine)
    chemin = dossier_mr(racine) / f"{ident}.md"
    if not chemin.exists():
        sys.exit(f"Pas de merge request pour {ident}.")
    texte = chemin.read_text(encoding="utf-8")
    statut = lire_champ(texte, "Statut")
    branche = (lire_champ(texte, "Branche") or "").split(" → ")[0]
    if statut == FUSIONNEE:
        sys.exit(f"La merge request de {ident} est déjà fusionnée.")
    if statut != PRETE:
        sys.exit(f"Fusion refusée : la merge request de {ident} est en brouillon. GitLab refuse aussi de fusionner "
                 "un brouillon. Lancer /ship-dev sur la branche pour la passer « Prête à relire ».")
    tete = git("rev-parse", "--verify", "--quiet", f"refs/heads/{branche}", cwd=distant, verifier=False).stdout.strip()
    if not tete:
        sys.exit(f"La branche {branche} n'est pas sur le dépôt distant.")
    main = git("rev-parse", "refs/heads/main", cwd=distant).stdout.strip()
    r = git("merge-tree", "--write-tree", "--name-only", main, tete, cwd=distant, verifier=False)
    if r.returncode == 1:
        fichiers = [ligne for ligne in r.stdout.splitlines()[1:] if ligne and not ligne.startswith(("Auto-merging", "CONFLICT"))]
        sys.exit(f"Fusion refusée : la branche {branche} est en conflit avec main ({', '.join(fichiers) or 'voir git'}).\n"
                 "Comme sur GitLab, il faut d'abord récupérer main dans la branche : lancer /sync-dev sur le ticket, "
                 "puis relancer la fusion.")
    if r.returncode != 0:
        sys.exit(f"Erreur : git merge-tree\n{r.stderr.strip()}")
    arbre = r.stdout.splitlines()[0].strip()
    nom = git("config", "user.name", cwd=racine, verifier=False).stdout.strip() or "Personne qui relit"
    courriel = git("config", "user.email", cwd=racine, verifier=False).stdout.strip() or "relecture@exemple.invalid"
    titre = texte.splitlines()[0].lstrip("# ").strip()
    commit = subprocess.run(
        ["git", "-c", f"user.name={nom}", "-c", f"user.email={courriel}", "commit-tree", arbre,
         "-p", main, "-p", tete, "-m", f"Fusionne {branche} : {titre}"],
        cwd=distant, capture_output=True, text=True, check=True).stdout.strip()
    git("update-ref", "refs/heads/main", commit, main, cwd=distant)
    git("update-ref", "-d", f"refs/heads/{branche}", tete, cwd=distant)
    texte = changer_champ(texte, "Statut", FUSIONNEE)
    texte = texte.replace(f"- Statut : {FUSIONNEE}",
                          f"- Statut : {FUSIONNEE}\n- Fusionnée le : {dt.datetime.now():%d/%m/%Y à %H:%M} par {nom}", 1)
    chemin.write_text(texte, encoding="utf-8")
    print(f"Merge request de {ident} fusionnée dans main sur le dépôt distant (commit {commit[:7]}).")
    print(f"Branche {branche} supprimée sur le dépôt distant (la case « Delete source branch » de GitLab).")
    print(f"Sur le poste : /close-dev {ident} fait le ménage.")


def main() -> None:
    racine = racine_du_kit()
    args = sys.argv[1:]
    if not args:
        lister(racine)
    elif args[0] == "ouvrir" and len(args) == 4:
        ouvrir(racine, args[1].upper(), args[2], args[3])
    elif args[0] == "prete" and len(args) == 2:
        prete(racine, args[1].upper())
    elif args[0] == "fusionner" and len(args) == 2:
        fusionner(racine, args[1].upper())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
