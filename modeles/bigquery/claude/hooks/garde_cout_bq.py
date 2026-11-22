"""Hook PreToolUse : garde-fou de coût et de lecture seule pour BigQuery (outil bq).

Refuse :
  - une requête « bq query » lancée sans --dry_run et sans --maximum_bytes_billed ;
  - un plafond --maximum_bytes_billed supérieur à PLAFOND_OCTETS ;
  - une requête qui écrit ou modifie (INSERT, UPDATE, DELETE, MERGE, CREATE, DROP, ALTER, TRUNCATE) ;
  - les commandes bq qui modifient (rm, mk, load, cp, update, insert, truncate).
Le dry run (estimation du volume lu, gratuite) est toujours permis.

À adapter : PLAFOND_OCTETS, et MOTS_INTERDITS si un projet doit créer des modèles (CREATE MODEL) dans un
dataset de travail : dans ce cas, autoriser seulement ce dataset.
"""

from __future__ import annotations

import json
import re
import shlex
import sys

PLAFOND_OCTETS = 5_000_000_000          # 5 Go par requête
MOTS_INTERDITS = r"\b(INSERT|UPDATE|DELETE|MERGE|CREATE|DROP|ALTER|TRUNCATE)\b"
SOUS_COMMANDES_INTERDITES = {"rm", "mk", "load", "cp", "update", "insert", "truncate"}


def refuser(raison: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": raison}}, ensure_ascii=False))
    sys.exit(0)


def segments(commande: str) -> list[list[str]]:
    resultat = []
    for m in re.split(r"&&|\|\||[;\n]", commande):
        try:
            jetons = shlex.split(m)
        except ValueError:
            jetons = m.split()
        if jetons:
            resultat.append(jetons)
    return resultat


def verifier_bq(j: list[str]) -> None:
    i = j.index("bq")
    reste = [a for a in j[i + 1:]]
    sous = next((a for a in reste if not a.startswith("-")), "")
    if sous in SOUS_COMMANDES_INTERDITES:
        refuser(f"Refusé par le garde-fou BigQuery : « bq {sous} » modifie des données. Ici, lecture seule.")
    if sous != "query":
        return
    texte = " ".join(reste)
    if re.search(MOTS_INTERDITS, texte, flags=re.IGNORECASE):
        refuser("Refusé par le garde-fou BigQuery : la requête écrit ou modifie des données. Ici, lecture seule.")
    if any(a == "--dry_run" or a.startswith("--dry_run=") and a != "--dry_run=false" for a in reste):
        return
    plafond = None
    for k, a in enumerate(reste):
        if a.startswith("--maximum_bytes_billed"):
            valeur = a.split("=", 1)[1] if "=" in a else (reste[k + 1] if k + 1 < len(reste) else "")
            try:
                plafond = int(valeur)
            except ValueError:
                refuser("Refusé par le garde-fou BigQuery : --maximum_bytes_billed doit être un nombre d'octets.")
    if plafond is None:
        refuser("Refusé par le garde-fou BigQuery : lancez d'abord la requête avec --dry_run pour estimer le volume "
                f"lu, puis exécutez-la avec --maximum_bytes_billed (au plus {PLAFOND_OCTETS:_} octets).".replace("_", " "))
    if plafond > PLAFOND_OCTETS:
        refuser(f"Refusé par le garde-fou BigQuery : plafond trop haut ({plafond:_} octets). "
                f"Maximum permis : {PLAFOND_OCTETS:_}. Filtrez la partition (date) ou demandez à un humain.".replace("_", " "))


def main() -> None:
    try:
        d = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    if d.get("tool_name") != "Bash":
        sys.exit(0)
    commande = (d.get("tool_input") or {}).get("command") or ""
    for j in segments(commande):
        if "bq" in j:
            verifier_bq(j)
    sys.exit(0)


if __name__ == "__main__":
    main()
