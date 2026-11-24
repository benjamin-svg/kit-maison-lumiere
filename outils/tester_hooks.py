"""Vérifie que les hooks de .claude/settings.json se comportent comme prévu.

Usage : uv run python outils/tester_hooks.py

Chaque cas envoie au hook le JSON que Claude Code lui enverrait, en lançant la commande
exactement telle qu'elle est écrite dans .claude/settings.json.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGLAGES = json.loads((RACINE / ".claude" / "settings.json").read_text(encoding="utf-8"))


def commande_hook(evenement: str) -> str:
    return REGLAGES["hooks"][evenement][0]["hooks"][0]["command"]


def appeler(evenement: str, outil: str, entree: dict) -> tuple[int, str, str]:
    charge = {"session_id": "test", "cwd": str(RACINE), "hook_event_name": evenement,
              "tool_name": outil, "tool_input": entree}
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(RACINE))
    r = subprocess.run(["bash", "-c", commande_hook(evenement)], input=json.dumps(charge),
                       capture_output=True, text=True, env=env, cwd=RACINE, timeout=200)
    return r.returncode, r.stdout, r.stderr


def refuse(sortie: str) -> bool:
    try:
        return json.loads(sortie)["hookSpecificOutput"]["permissionDecision"] == "deny"
    except (json.JSONDecodeError, KeyError, TypeError):
        return False


CAS_PRE = [
    # (description, outil, entrée, doit être refusé)
    ("Write dans donnees/brutes", "Write", {"file_path": str(RACINE / "donnees/brutes/produits.csv"), "content": "x"}, True),
    ("Edit relatif dans donnees/brutes", "Edit", {"file_path": "donnees/brutes/clients.csv", "old_string": "a", "new_string": "b"}, True),
    ("Edit avec ../ vers brutes", "Edit", {"file_path": "travail/../donnees/brutes/clients.csv", "old_string": "a", "new_string": "b"}, True),
    ("Write dans travail/", "Write", {"file_path": str(RACINE / "travail/celine/note.md"), "content": "x"}, False),
    ("Edit du générateur (hors brutes)", "Edit", {"file_path": "donnees/generer_donnees.py", "old_string": "a", "new_string": "b"}, False),
    ("rm -rf", "Bash", {"command": "rm -rf travail/test"}, True),
    ("rm -fr", "Bash", {"command": "rm -fr /tmp/x"}, True),
    ("rm -r -f", "Bash", {"command": "cd travail && rm -r -f vieux"}, True),
    ("rm -Rf après &&", "Bash", {"command": "ls && rm -Rf build"}, True),
    ("rm --recursive --force", "Bash", {"command": "rm --recursive --force dossier"}, True),
    ("sudo rm -rf", "Bash", {"command": "sudo rm -rf /"}, True),
    ("rm simple (permis)", "Bash", {"command": "rm travail/celine/brouillon.txt"}, False),
    ("rm -r sans -f (permis)", "Bash", {"command": "rm -r travail/celine/essai"}, False),
    ("redirection vers brutes", "Bash", {"command": "echo test > donnees/brutes/produits.csv"}, True),
    ("ajout vers brutes", "Bash", {"command": "cat x.csv >> ./donnees/brutes/clients.csv"}, True),
    ("sed -i sur brutes", "Bash", {"command": "sed -i 's/a/b/' donnees/brutes/produits.csv"}, True),
    ("fusionner une merge request", "Bash", {"command": "uv run python outils/merge_request.py fusionner T-100"}, True),
    ("passer une merge request prête (permis)", "Bash", {"command": "uv run python outils/merge_request.py prete T-100"}, False),
    ("mv depuis brutes", "Bash", {"command": "mv donnees/brutes/emails.csv /tmp/"}, True),
    ("cp vers brutes", "Bash", {"command": "cp travail/x.csv donnees/brutes/"}, True),
    ("pandas to_csv vers brutes", "Bash", {"command": "uv run python -c \"import pandas as pd; pd.DataFrame().to_csv('donnees/brutes/x.csv')\""}, True),
    ("lecture de brutes (permis)", "Bash", {"command": "head -5 donnees/brutes/produits.csv"}, False),
    ("cp depuis brutes vers travail (permis)", "Bash", {"command": "cp donnees/brutes/produits.csv travail/celine/"}, False),
    ("requête DuckDB (permis)", "Bash", {"command": "uv run python outils/requete.py \"SELECT COUNT(*) FROM commandes\""}, False),
    ("génération des données (permis)", "Bash", {"command": "uv run python donnees/generer_donnees.py"}, False),
    ("lecture du corrigé par Bash", "Bash", {"command": "cat exercices/corrige-formateur.md"}, True),
    ("git status (permis)", "Bash", {"command": "git status"}, False),
    ("Read d'une fiche d'exercice", "Read", {"file_path": str(RACINE / "exercices/05-ml-churn.md")}, True),
    ("cat d'une fiche d'exercice", "Bash", {"command": "cat exercices/05-ml-churn.md"}, True),
    ("grep dans exercices/", "Bash", {"command": "grep -n fuite exercices/*.md"}, True),
    ("Grep sur le dossier exercices", "Grep", {"pattern": "fuite", "path": "exercices"}, True),
    ("ls exercices (permis)", "Bash", {"command": "ls exercices/"}, False),
    ("Read du générateur", "Read", {"file_path": "donnees/generer_donnees.py"}, True),
    ("sed sur le générateur", "Bash", {"command": "sed -n 1,80p donnees/generer_donnees.py"}, True),
    ("Read d'une fiche sémantique (permis)", "Read", {"file_path": "semantique/tables/clients.md"}, False),
]


def main() -> int:
    echecs = 0
    print("PreToolUse (garde_fou.py)")
    for desc, outil, entree, attendu in CAS_PRE:
        code, sortie, err = appeler("PreToolUse", outil, entree)
        obtenu = refuse(sortie)
        ok = obtenu == attendu and code == 0
        echecs += not ok
        print(f"  [{'OK' if ok else 'ÉCHEC'}] {desc} : {'refusé' if obtenu else 'autorisé'}")
        if not ok:
            print(f"        code={code} sortie={sortie!r} erreurs={err[-300:]!r}")

    print("PostToolUse (lancer_tests.py)")
    fichier = RACINE / "projets/portail/app/delais.py"
    code, sortie, err = appeler("PostToolUse", "Edit", {"file_path": str(fichier), "old_string": "a", "new_string": "b"})
    ok = code == 0 and "passed" in sortie
    echecs += not ok
    print(f"  [{'OK' if ok else 'ÉCHEC'}] modification d'un .py du portail : tests lancés -> {sortie.strip()[:160]}")
    code, sortie, err = appeler("PostToolUse", "Write", {"file_path": str(RACINE / "travail/celine/x.py"), "content": ""})
    ok = code == 0 and sortie.strip() == ""
    echecs += not ok
    print(f"  [{'OK' if ok else 'ÉCHEC'}] modification hors de projets/ : aucun test lancé")
    code, sortie, err = appeler("PostToolUse", "Edit", {"file_path": str(RACINE / "projets/portail/CLAUDE.md")})
    ok = code == 0 and sortie.strip() == ""
    echecs += not ok
    print(f"  [{'OK' if ok else 'ÉCHEC'}] modification d'un fichier non Python : aucun test lancé")

    # Test qui échoue : on crée un faux projet temporaire
    faux = RACINE / "projets" / "_essai_hook"
    (faux / "tests").mkdir(parents=True, exist_ok=True)
    (faux / "tests" / "test_rouge.py").write_text("def test_rouge():\n    assert 1 == 2\n", encoding="utf-8")
    try:
        code, sortie, err = appeler("PostToolUse", "Write", {"file_path": str(faux / "tests" / "test_rouge.py")})
        ok = code == 2 and "échouent" in err
        echecs += not ok
        print(f"  [{'OK' if ok else 'ÉCHEC'}] test en échec : le hook le signale à Claude (code 2)")
    finally:
        shutil.rmtree(faux, ignore_errors=True)

    print(f"\n{'Tous les cas sont conformes.' if not echecs else f'{echecs} cas non conformes.'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
