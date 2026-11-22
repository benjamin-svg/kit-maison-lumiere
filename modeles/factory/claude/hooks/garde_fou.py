"""Hook PreToolUse : refuse quelques actions dangereuses, quel que soit le projet.

Refuse :
  - les suppressions récursives forcées (rm -rf et ses variantes) ;
  - les poussées forcées (--force, -f, -uf, +branche), --all, --mirror, la suppression de branche distante,
    et toute poussée sur main (nommée, ou implicite depuis main) ;
  - la lecture ou la modification des fichiers de secrets (.env, *.key, *.pem).
À compléter avec les règles propres à votre projet (dossiers en lecture seule, commandes coûteuses...).
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys

BRANCHE_PRINCIPALE = "main"
MOTIF_SECRETS = r"(^|[/\\\s\"'])(\.env(\.[\w-]+)?|[\w-]+\.(key|pem))(\s|$|[\"'])"


def refuser(raison: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": raison}}, ensure_ascii=False))
    sys.exit(0)


def segments(commande: str) -> list[list[str]]:
    resultat = []
    for m in re.split(r"&&|\|\||[;|\n]", commande):
        try:
            jetons = shlex.split(m)
        except ValueError:
            jetons = m.split()
        if jetons:
            resultat.append(jetons)
    return resultat


def est_rm_rf(j: list[str]) -> bool:
    while j and j[0] in {"sudo", "command", "env", "xargs", "nohup", "time", "exec"}:
        j = j[1:]
    if not j or j[0].rsplit("/", 1)[-1] != "rm":
        return False
    r = f = False
    for a in j[1:]:
        if a == "--":
            break
        if a.startswith("--"):
            r |= a == "--recursive"
            f |= a == "--force"
        elif a.startswith("-"):
            r |= "r" in a or "R" in a
            f |= "f" in a
    return r and f


def branche_courante(dossier: str | None) -> str:
    try:
        r = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=dossier or None,
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def poussee_interdite(j: list[str], dossier: str | None = None) -> str | None:
    # On saute les options globales de git (git -C dossier push, git -c cle=valeur push).
    if not j or j[0] != "git":
        return None
    i = 1
    while i < len(j) and j[i] in {"-C", "-c"}:
        i += 2
    if i >= len(j) or j[i] != "push":
        return None
    args = j[i + 1:]
    options = [a for a in args if a.startswith("-")]
    forcee = any(a.startswith("--force") for a in options) or \
        any(not a.startswith("--") and "f" in a[1:] for a in options) or \
        any(a.startswith("+") for a in args if not a.startswith("-"))
    if forcee:
        return "Refusé par le garde-fou : pas de poussée forcée (--force, -f ou +branche)."
    if any(a in {"--all", "--mirror", "--delete", "-d"} for a in options):
        return "Refusé par le garde-fou : pas de poussée de toutes les branches ni de suppression de branche."
    cibles = [a for a in args if not a.startswith("-")][1:]  # le premier est le dépôt distant
    noms = {BRANCHE_PRINCIPALE, "refs/heads/" + BRANCHE_PRINCIPALE}
    if any(c in noms or c.split(":")[-1] in noms for c in cibles):
        return (f"Refusé par le garde-fou : on ne pousse pas directement sur {BRANCHE_PRINCIPALE}. "
                "Poussez une branche et ouvrez une merge request.")
    # Sans branche nommée, git pousse la branche courante : on vérifie que ce n'est pas main.
    if not cibles and branche_courante(dossier) == BRANCHE_PRINCIPALE:
        return (f"Refusé par le garde-fou : vous êtes sur {BRANCHE_PRINCIPALE}. "
                "Créez une branche, poussez-la et ouvrez une merge request.")
    return None


def main() -> None:
    try:
        d = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    outil = d.get("tool_name", "")
    entree = d.get("tool_input") or {}
    if outil == "Bash":
        commande = entree.get("command") or ""
        for j in segments(commande):
            if est_rm_rf(j):
                refuser("Refusé par le garde-fou : pas de suppression récursive forcée (rm -rf).")
            raison = poussee_interdite(j, d.get("cwd"))
            if raison:
                refuser(raison)
        if re.search(MOTIF_SECRETS, commande):
            refuser("Refusé par le garde-fou : les fichiers de secrets (.env, clés) ne se lisent pas ici.")
    elif outil in {"Read", "Write", "Edit", "MultiEdit"}:
        chemin = entree.get("file_path") or ""
        if re.search(MOTIF_SECRETS, " " + chemin + " "):
            refuser("Refusé par le garde-fou : les fichiers de secrets (.env, clés) ne se lisent pas ici.")
    sys.exit(0)


if __name__ == "__main__":
    main()
