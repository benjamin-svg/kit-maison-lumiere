"""Vérifie le garde-fou de la software factory sans rien pousser : python3 tester_garde_fou.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "claude" / "hooks" / "garde_fou.py"


def depot_sur(branche: str) -> str:
    d = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", "-b", branche, d], check=True)
    return d


SUR_MAIN = depot_sur("main")
SUR_BRANCHE = depot_sur("ticket/T-1-essai")

CAS = [
    ("rm -rf", "rm -rf dossier", SUR_BRANCHE, True),
    ("rm -r sans -f (permis)", "rm -r dossier", SUR_BRANCHE, False),
    ("poussée forcée --force", "git push --force origin ticket/T-1", SUR_BRANCHE, True),
    ("poussée forcée -f", "git push -f origin ticket/T-1", SUR_BRANCHE, True),
    ("poussée forcée -uf", "git push -uf origin ticket/T-1", SUR_BRANCHE, True),
    ("poussée forcée --force-with-lease", "git push --force-with-lease", SUR_BRANCHE, True),
    ("poussée forcée +main", "git push origin +main", SUR_BRANCHE, True),
    ("poussée forcée +x:main", "git push origin +x:main", SUR_BRANCHE, True),
    ("poussée sur main nommée", "git push origin main", SUR_BRANCHE, True),
    ("poussée HEAD:main", "git push origin HEAD:main", SUR_BRANCHE, True),
    ("poussée refs/heads/main", "git push origin x:refs/heads/main", SUR_BRANCHE, True),
    ("git -C ... push origin main", "git -C . push origin main", SUR_BRANCHE, True),
    ("git push depuis main", "git push", SUR_MAIN, True),
    ("git push origin depuis main", "git push origin", SUR_MAIN, True),
    ("git push --all", "git push --all origin", SUR_BRANCHE, True),
    ("suppression de branche distante", "git push origin --delete ticket/T-1", SUR_BRANCHE, True),
    ("poussée d'une branche (permis)", "git push -u origin ticket/T-1-essai", SUR_BRANCHE, False),
    ("git push depuis une branche (permis)", "git push", SUR_BRANCHE, False),
    ("lecture de .env", "cat .env", SUR_BRANCHE, True),
    ("git status (permis)", "git status", SUR_MAIN, False),
]


def refuse(commande: str, dossier: str) -> bool:
    entree = {"tool_name": "Bash", "tool_input": {"command": commande}, "cwd": dossier}
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(entree), capture_output=True, text=True)
    return bool(r.stdout.strip()) and json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


echecs = 0
for desc, commande, dossier, attendu in CAS:
    ok = refuse(commande, dossier) == attendu
    echecs += not ok
    print(f"[{'OK' if ok else 'ÉCHEC'}] {desc}")
print("Tous les cas sont conformes." if not echecs else f"{echecs} cas non conformes.")
sys.exit(1 if echecs else 0)
