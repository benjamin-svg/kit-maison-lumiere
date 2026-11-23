"""Hook PostToolUse : relance les tests d'un projet après la modification d'un de ses fichiers Python.

Règle : si le fichier modifié est un .py situé sous projets/<nom>/, on lance « uv run pytest -q »
dans projets/<nom>/ (s'il contient des tests). En cas d'échec, le résumé est renvoyé à Claude
(code de sortie 2) pour qu'il en tienne compte ; en cas de succès, Claude reçoit une ligne de résumé.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]


def projet_concerne(chemin: str, cwd: str) -> Path | None:
    """Le dossier projets/<nom>/ du fichier modifié, dans le kit ou dans un worktree (.worktrees/<ticket>/)."""
    p = Path(chemin)
    if not p.is_absolute():
        p = Path(cwd) / p
    p = p.resolve()
    if p.suffix != ".py":
        return None
    racines = [RACINE.resolve()]
    worktrees = RACINE / ".worktrees"
    if worktrees.is_dir():
        racines += [d.resolve() for d in worktrees.iterdir() if d.is_dir()]
    for racine in sorted(racines, key=lambda r: len(r.parts), reverse=True):
        projets = racine / "projets"
        if projets in p.parents:
            return projets / p.relative_to(projets).parts[0]
    return None


def contient_des_tests(projet: Path) -> bool:
    for f in projet.rglob("*.py"):
        if any(part.startswith(".") or part in {"__pycache__", "node_modules"}
               for part in f.relative_to(projet).parts):
            continue
        if f.name.startswith("test_") or f.name.endswith("_test.py"):
            return True
    return False


def main() -> None:
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    entree = donnees.get("tool_input", {}) or {}
    chemin = entree.get("file_path") or ""
    if not chemin:
        sys.exit(0)
    projet = projet_concerne(chemin, donnees.get("cwd") or os.getcwd())
    if projet is None or not projet.is_dir() or not contient_des_tests(projet):
        sys.exit(0)

    uv = shutil.which("uv")
    commande = [uv, "run", "pytest", "-q"] if uv else [sys.executable, "-m", "pytest", "-q"]
    try:
        r = subprocess.run(commande, cwd=projet, capture_output=True, text=True, timeout=170)
    except subprocess.TimeoutExpired:
        print(f"Tests de {projet.name} : délai dépassé (170 s).", file=sys.stderr)
        sys.exit(2)
    sortie = (r.stdout + r.stderr).strip().splitlines()
    lignes_pytest = r.stdout.strip().splitlines()
    resume = next((l for l in reversed(lignes_pytest)
                   if any(m in l for m in ("passed", "failed", "error", "no tests"))),
                  lignes_pytest[-1] if lignes_pytest else "")
    nom = projet.relative_to(RACINE.resolve()).as_posix()

    if r.returncode in (0, 5):  # 5 = aucun test collecté
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Hook : tests de {nom} relancés automatiquement : {resume}",
        }}, ensure_ascii=False))
        sys.exit(0)

    extrait = "\n".join(lignes_pytest[-60:] or sortie[-60:])
    print(f"Hook : les tests de {nom} échouent après cette modification ({resume}).\n"
          f"Si vous venez d'écrire un test qui doit échouer (retour de recette), c'est attendu ; "
          f"sinon, corrigez avant de continuer.\n\n{extrait}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
