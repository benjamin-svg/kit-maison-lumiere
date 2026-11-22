"""Vérifie le garde-fou de coût BigQuery sans BigQuery : python3 tester_garde_cout.py"""

import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "claude" / "hooks" / "garde_cout_bq.py"
CAS = [
    ("dry run", "bq query --use_legacy_sql=false --dry_run 'SELECT 1'", False),
    ("exécution avec plafond", "bq query --use_legacy_sql=false --maximum_bytes_billed=1000000000 'SELECT 1'", False),
    ("exécution sans plafond", "bq query --use_legacy_sql=false 'SELECT 1'", True),
    ("plafond trop haut", "bq query --use_legacy_sql=false --maximum_bytes_billed=900000000000 'SELECT 1'", True),
    ("requête qui supprime", "bq query --use_legacy_sql=false --maximum_bytes_billed=10 'DELETE FROM t WHERE 1=1'", True),
    ("création de table", "bq query --use_legacy_sql=false --dry_run 'CREATE TABLE x AS SELECT 1'", True),
    ("bq rm", "bq rm -f projet:dataset.table", True),
    ("bq ls (permis)", "bq ls projet:dataset", False),
    ("bq show (permis)", "bq show --schema projet:dataset.table", False),
    ("autre commande (permis)", "git status", False),
]


def refuse(commande: str) -> bool:
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": commande}}),
                       capture_output=True, text=True)
    return bool(r.stdout.strip()) and json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


echecs = 0
for desc, commande, attendu in CAS:
    ok = refuse(commande) == attendu
    echecs += not ok
    print(f"[{'OK' if ok else 'ÉCHEC'}] {desc}")
print("Tous les cas sont conformes." if not echecs else f"{echecs} cas non conformes.")
sys.exit(1 if echecs else 0)
