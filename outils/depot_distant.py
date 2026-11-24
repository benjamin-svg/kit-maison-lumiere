"""Prépare le dépôt distant du kit (démonstration 3), qui joue le rôle de GitLab.

Le kit n'a pas de vrai GitLab. Ce script crée, dans le dossier caché `.depot-distant/`, un dépôt
« nu » (sans fichiers de travail, comme celui d'un serveur), le déclare comme dépôt distant `origin`,
puis y envoie la branche `main`. Ensuite, `git pull`, `git push` et `git fetch` marchent comme avec GitLab.

Usage (depuis le dossier du kit) :
    uv run python outils/depot_distant.py            # prépare, ou vérifie que tout est prêt
    uv run python outils/depot_distant.py --etat     # affiche seulement l'état

Si le kit a déjà un dépôt distant `origin` (par exemple un vrai GitLab), le script ne change rien :
la démonstration se fait alors dans une copie du kit tirée de l'archive.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def git(*args: str, cwd: Path, verifier: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if verifier and r.returncode != 0:
        print(f"Erreur : git {' '.join(args)}\n{r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return r


def racine_du_kit() -> Path:
    """Dossier principal du kit, même si l'on est dans un worktree."""
    ici = Path(__file__).resolve().parent
    commun = git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=ici).stdout.strip()
    return Path(commun).parent


def chemin_distant(racine: Path) -> Path:
    return racine / ".depot-distant" / "kit-maison-lumiere.git"


def url_origin(racine: Path) -> str | None:
    r = git("remote", "get-url", "origin", cwd=racine, verifier=False)
    return r.stdout.strip() if r.returncode == 0 else None


def est_le_distant_simule(url: str | None, racine: Path) -> bool:
    if not url:
        return False
    try:
        return Path(url).resolve() == chemin_distant(racine).resolve()
    except OSError:
        return False


def main() -> None:
    racine = racine_du_kit()
    distant = chemin_distant(racine)
    url = url_origin(racine)

    if "--etat" in sys.argv:
        if est_le_distant_simule(url, racine):
            print(f"Prêt : origin = {distant}")
        elif url:
            print(f"Ce kit a un autre dépôt distant : origin = {url}")
        else:
            print("Pas encore de dépôt distant. Lancer : uv run python outils/depot_distant.py")
        return

    if url and not est_le_distant_simule(url, racine):
        print(
            f"Ce kit a déjà un dépôt distant : origin = {url}\n"
            "Je ne change rien. Pour la démonstration 3, utilisez une copie du kit tirée de l'archive :\n"
            "le dépôt distant simulé ne doit pas remplacer un vrai GitLab.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not distant.exists():
        distant.parent.mkdir(parents=True, exist_ok=True)
        git("init", "--bare", "--initial-branch=main", str(distant), cwd=racine)
        print(f"Dépôt distant créé : {distant.relative_to(racine)}")
    if not url:
        git("remote", "add", "origin", str(distant), cwd=racine)
        print("Déclaré comme dépôt distant « origin ».")

    if not git("ls-remote", "--heads", "origin", "main", cwd=racine).stdout.strip():
        git("push", "--quiet", "-u", "origin", "main", cwd=racine)
        print("Branche main envoyée sur le dépôt distant.")
    print("Prêt : le dépôt distant joue le rôle de GitLab pour la démonstration 3.")


if __name__ == "__main__":
    main()
