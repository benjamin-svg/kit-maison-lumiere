"""Simule un collègue qui fait fusionner une petite correction dans main, sur le dépôt distant.

Exercice 02, étape 3. Pendant que vous travaillez sur votre ticket, « Olivier » corrige la page
d'accueil du portail : il précise la date prévue de l'application de ciblage. Sa correction arrive
dans `main` sur le dépôt distant. Votre branche ne la contient pas encore : c'est le travail de /sync-dev.

Le script travaille dans une copie temporaire du dépôt distant : il ne touche ni à vos fichiers,
ni à vos branches. Il ne marche qu'avec le dépôt distant simulé du kit (voir outils/depot_distant.py),
jamais avec un vrai GitLab.

Usage (depuis le dossier du kit) :
    uv run python outils/simuler_collegue.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depot_distant import chemin_distant, est_le_distant_simule, racine_du_kit, url_origin  # noqa: E402

FICHIER = Path("projets/portail/app/applications.py")
AVANT = "Liste des clients susceptibles de ne plus commander (projet en cours)."
APRES = "Liste des clients susceptibles de ne plus commander (projet en cours, prévu pour mars)."
AUTEUR = ["-c", "user.name=Olivier (collègue simulé)", "-c", "user.email=olivier@exemple.invalid"]
MESSAGE = "Précise la date prévue du ciblage sur l'accueil"


def git(*args: str, cwd: Path) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Erreur : git {' '.join(args)}\n{r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def main() -> None:
    racine = racine_du_kit()
    if not est_le_distant_simule(url_origin(racine), racine):
        print(
            "Le dépôt distant simulé n'est pas prêt (ou ce kit utilise un vrai GitLab).\n"
            "Lancer d'abord : uv run python outils/depot_distant.py",
            file=sys.stderr,
        )
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="collegue-") as dossier:
        copie = Path(dossier) / "kit"
        git("clone", "--quiet", "--branch", "main", str(chemin_distant(racine)), str(copie), cwd=racine)
        cible = copie / FICHIER
        texte = cible.read_text(encoding="utf-8")
        if APRES in texte:
            print("La correction du collègue est déjà dans main sur le dépôt distant. Rien à faire.")
            return
        if AVANT not in texte:
            print(f"Je ne trouve pas le texte attendu dans {FICHIER} : je ne change rien.", file=sys.stderr)
            sys.exit(1)
        cible.write_text(texte.replace(AVANT, APRES), encoding="utf-8")
        git(*AUTEUR, "commit", "--quiet", "-am", MESSAGE, cwd=copie)
        git("push", "--quiet", "origin", "main", cwd=copie)
        commit = git("log", "-1", "--format=%h %an : %s", cwd=copie)

    print("Un collègue vient de faire fusionner une correction dans main, sur le dépôt distant.")
    print(f"  Commit : {commit}")
    print(f"  Fichier : {FICHIER} (description de l'application de ciblage, page d'accueil)")
    print("Votre branche ne la contient pas encore. Tapez /sync-dev pour la récupérer.")


if __name__ == "__main__":
    main()
