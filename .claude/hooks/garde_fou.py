"""Hook PreToolUse : garde-fou de la formation.

Refuse :
  - toute écriture (Write, Edit, NotebookEdit ou commande Bash) dans donnees/brutes/ ;
  - toute commande « rm » à la fois récursive et forcée (rm -rf, rm -fr, rm -r -f, rm --recursive --force...) ;
  - toute lecture des fiches d'exercice (exercices/) : elles sont pour le participant, pas pour Claude ;
  - toute lecture du script de génération des données (sur les vraies données, il n'existe pas) ;
    le lancer reste permis.

Entrée : le JSON envoyé par Claude Code sur l'entrée standard.
Sortie : un JSON « permissionDecision: deny » si l'action est refusée, rien sinon.
Ce garde-fou est un filet de sécurité pédagogique, pas une protection absolue.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
BRUTES = (RACINE / "donnees" / "brutes").resolve()
# Les worktrees de l'exercice 02 (.worktrees/<ticket>/) sont des copies du kit : mêmes interdits.
WORKTREES = (RACINE / ".worktrees").resolve()
MOTIF_BRUTES = r"donnees[/\\]+brutes"


def refuser(raison: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": raison,
        }
    }, ensure_ascii=False))
    sys.exit(0)


def dans_brutes(chemin: str, cwd: str) -> bool:
    p = Path(chemin)
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        p = p.resolve()
    except OSError:
        return False
    return any(p == b or b in p.parents for b in (BRUTES, *[r / "donnees" / "brutes" for r in copies()]))


def copies() -> list[Path]:
    """Les dossiers des worktrees, s'il y en a."""
    if not WORKTREES.is_dir():
        return []
    return [d.resolve() for d in WORKTREES.iterdir() if d.is_dir()]


def segments(commande: str) -> list[list[str]]:
    """Découpe une commande en sous-commandes (séparées par ; && || | et retours à la ligne)."""
    morceaux = re.split(r"&&|\|\||[;|\n]", commande)
    resultat = []
    for m in morceaux:
        try:
            jetons = shlex.split(m, posix=True)
        except ValueError:
            jetons = m.split()
        if jetons:
            resultat.append(jetons)
    return resultat


def est_rm_rf(jetons: list[str]) -> bool:
    # ignorer les préfixes courants (sudo, env, command, xargs...)
    i = 0
    while i < len(jetons) and jetons[i] in {"sudo", "command", "env", "xargs", "nohup", "time", "exec"}:
        i += 1
    if i >= len(jetons) or Path(jetons[i]).name != "rm":
        return False
    recursif = force = False
    for j in jetons[i + 1:]:
        if j == "--":
            break
        if j.startswith("--"):
            recursif |= j == "--recursive"
            force |= j == "--force"
        elif j.startswith("-") and len(j) > 1:
            recursif |= ("r" in j[1:]) or ("R" in j[1:])
            force |= "f" in j[1:]
    return recursif and force


MOTIFS_ECRITURE_BASH = [
    rf">{{1,2}}\s*[\"']?[^\s;|&]*{MOTIF_BRUTES}",                       # redirection vers brutes
    rf"\b(rm|rmdir|unlink|mv|touch|tee|truncate|shred|chmod|chown|ln|install|dd)\b[^;|&\n]*{MOTIF_BRUTES}",
    rf"\bsed\b[^;|&\n]*\s-i[^;|&\n]*{MOTIF_BRUTES}",
    rf"\bsed\b[^;|&\n]*{MOTIF_BRUTES}[^;|&\n]*\s-i\b",
    rf"\b(to_csv|to_parquet|to_excel|write_text|write_bytes|unlink|rmtree|remove|rename|replace)\b[^;\n]*{MOTIF_BRUTES}",
    rf"{MOTIF_BRUTES}[^;\n]*\b(to_csv|to_parquet|write_text|write_bytes|unlink|rmtree)\b",
    rf"open\([^)]*{MOTIF_BRUTES}[^)]*,\s*[\"'][wax]",
    rf"\bCOPY\b[^;]*\bTO\b[^;]*{MOTIF_BRUTES}",
]


def ecrit_dans_brutes_bash(commande: str) -> bool:
    if not re.search(MOTIF_BRUTES, commande):
        return False
    for motif in MOTIFS_ECRITURE_BASH:
        if re.search(motif, commande, flags=re.IGNORECASE):
            return True
    # cp ou rsync dont la destination (dernier argument) est dans brutes
    for jetons in segments(commande):
        if Path(jetons[0]).name in {"cp", "rsync", "scp"} and re.search(MOTIF_BRUTES, jetons[-1]):
            return True
    return False


MOTIF_EXERCICES = r"(^|[\s\"'=:/\\])exercices([/\\]|$|\s)"
MOTIF_GENERATEUR = r"generer_donnees\.py"
LANCER_GENERATEUR = r"^\s*(uv run\s+)?(python3?\s+)?(\./)?donnees[/\\]generer_donnees\.py\s*$"
COMMANDES_PERMISES_EXERCICES = r"^\s*(ls|git\s+(status|log|add|commit|diff\s+--stat))\b"

MESSAGE_EXERCICES = ("Refusé par le garde-fou de la formation : les fiches d'exercice (exercices/) sont pour le "
                     "participant, pas pour Claude. Demandez-lui de vous donner la consigne.")
MESSAGE_GENERATEUR = ("Refusé par le garde-fou de la formation : le script de génération sert seulement à créer "
                      "les données fictives. Sur les vraies données, il n'existe pas : documentez les tables à partir "
                      "des données elles-mêmes (requêtes). Le lancer reste permis.")


def chemin_interdit_en_lecture(chemin: str, cwd: str) -> str | None:
    if not chemin:
        return None
    p = Path(chemin)
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        p = p.resolve()
    except OSError:
        return None
    for racine in (RACINE.resolve(), *copies()):
        exercices = racine / "exercices"
        if p == exercices or exercices in p.parents:
            return MESSAGE_EXERCICES
        if p == racine / "donnees" / "generer_donnees.py":
            return MESSAGE_GENERATEUR
    return None


def main() -> None:
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # entrée illisible : on laisse le circuit normal décider
    outil = donnees.get("tool_name", "")
    entree = donnees.get("tool_input", {}) or {}
    cwd = donnees.get("cwd") or os.getcwd()

    if outil in {"Read", "Grep", "Glob"}:
        for cle in ("file_path", "path"):
            raison = chemin_interdit_en_lecture(entree.get(cle) or "", cwd)
            if raison:
                refuser(raison)
        if outil == "Glob" and re.search(r"(^|/)exercices(/|$)", entree.get("pattern") or ""):
            refuser(MESSAGE_EXERCICES)
    elif outil in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
        chemin = entree.get("file_path") or entree.get("notebook_path") or ""
        if chemin and dans_brutes(chemin, cwd):
            refuser("Refusé par le garde-fou de la formation : le dossier donnees/brutes/ est en lecture seule. "
                    "Travaillez sur une copie dans travail/<prénom>/.")
    elif outil == "Bash":
        commande = entree.get("command", "") or ""
        if any(est_rm_rf(j) for j in segments(commande)):
            refuser("Refusé par le garde-fou de la formation : les suppressions récursives forcées (rm -rf) "
                    "sont interdites. Supprimez les fichiers un par un, ou demandez au formateur.")
        if ecrit_dans_brutes_bash(commande):
            refuser("Refusé par le garde-fou de la formation : cette commande semble modifier donnees/brutes/, "
                    "qui est en lecture seule. Lire ces fichiers est permis ; pour les transformer, "
                    "écrivez le résultat dans travail/<prénom>/.")
        if "corrige-formateur" in commande:
            refuser("Refusé : le corrigé est réservé au formateur.")
        if re.search(MOTIF_EXERCICES, commande) and not re.match(COMMANDES_PERMISES_EXERCICES, commande):
            refuser(MESSAGE_EXERCICES)
        if re.search(MOTIF_GENERATEUR, commande) and not re.match(LANCER_GENERATEUR, commande):
            refuser(MESSAGE_GENERATEUR)
    sys.exit(0)


if __name__ == "__main__":
    main()
