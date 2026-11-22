"""Hook PostToolUse : relance les tests après la modification d'un fichier de code.

À adapter en haut du fichier : la commande de tests et les extensions surveillées.
Branchement dans .claude/settings.json (voir settings.json à côté de ce dossier).

Comportement : succès -> une ligne de résumé est renvoyée à Claude ; échec -> code de sortie 2 et
l'extrait des tests est renvoyé à Claude, qui doit en tenir compte avant de continuer.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

# --- À ADAPTER ---------------------------------------------------------------
COMMANDE_TESTS = ["uv", "run", "pytest"]            # par exemple ["npm", "test"] ou ["mvn", "-q", "test"]
EXTENSIONS = {".py"}                                # par exemple {".ts", ".tsx"} ou {".java"}
DOSSIERS_IGNORES = {".venv", "node_modules", ".git", "__pycache__"}
DELAI_SECONDES = 170
# -----------------------------------------------------------------------------


def main() -> None:
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    chemin = (donnees.get("tool_input") or {}).get("file_path") or ""
    racine = Path(os.environ.get("CLAUDE_PROJECT_DIR") or donnees.get("cwd") or os.getcwd()).resolve()
    if not chemin:
        sys.exit(0)
    p = Path(chemin)
    if not p.is_absolute():
        p = Path(donnees.get("cwd") or racine) / p
    p = p.resolve()
    if p.suffix not in EXTENSIONS or racine not in p.parents:
        sys.exit(0)
    if any(part in DOSSIERS_IGNORES for part in p.relative_to(racine).parts):
        sys.exit(0)

    try:
        r = subprocess.run(COMMANDE_TESTS, cwd=racine, capture_output=True, text=True, timeout=DELAI_SECONDES)
    except subprocess.TimeoutExpired:
        print(f"Hook : les tests ont dépassé {DELAI_SECONDES} s.", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print(f"Hook : commande de tests introuvable ({COMMANDE_TESTS[0]}). Adaptez COMMANDE_TESTS.", file=sys.stderr)
        sys.exit(2)
    lignes = (r.stdout + r.stderr).strip().splitlines()
    sortie_tests = r.stdout.strip().splitlines()
    resume = next((l for l in reversed(sortie_tests) if any(m in l for m in ("passed", "failed", "error"))),
                  sortie_tests[-1] if sortie_tests else "aucune sortie")
    if r.returncode == 0:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Hook : tests relancés automatiquement : {resume}",
        }}, ensure_ascii=False))
        sys.exit(0)
    print("Hook : les tests échouent après cette modification. Si vous venez d'écrire un test qui doit échouer "
          "(retour de recette), c'est attendu ; sinon, corrigez avant de continuer.\n\n" + "\n".join(lignes[-60:]),
          file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
