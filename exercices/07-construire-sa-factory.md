# Exercice 07 - Construire son usine logicielle dans un dépôt neuf

## Objectif

À l'exercice 02, la chaîne était déjà montée. Ici, vous la construisez vous-même, brique par brique, dans un
dépôt qui ne contient rien pour Claude Code : c'est ce que vous referez lundi sur votre vrai portail.
À la fin, vous avez un dépôt prêt à pousser sur GitLab (exercice 08), et la liste de ce que vous devrez
adapter chez vous.

Le dépôt d'atelier (`modeles/depot-atelier/`) est une petite application Python (FastAPI). Si votre vrai
portail utilise une autre technique, la chaîne est la même : seule la commande de tests change.

## Durée

1 heure (parcours de Maxime) : étapes 0 à 5. L'étape 6 se fait en autonomie.

## Étape 0 - Partir d'un dépôt neuf, hors du kit (5 min)

Dans un terminal (pas dans Claude) :

```bash
cp -r modeles/depot-atelier ~/atelier-factory
cd ~/atelier-factory
git init -b main && git add . && git commit -m "État initial du dépôt d'atelier"
uv sync && uv run pytest
claude
```

Sous Windows, remplacez `~/atelier-factory` par un dossier de votre choix, par exemple `C:\atelier-factory`.

**À observer** : dans ce dossier, `/hooks`, `/agents` et `/` ne montrent rien du kit. Claude ne sait rien du projet.

**À savoir pour la suite** : Claude Code vous demande votre accord avant d'écrire dans `.claude/` (réglages,
hooks, sous-agents, skills), même en mode « Accepter les modifications ». C'est une protection voulue : ces
fichiers changent ce que Claude a le droit de faire. Relisez le fichier proposé, puis acceptez.

## Étape 1 - Le `CLAUDE.md` du projet (5 min)

> « Lis ce dépôt, puis interroge-moi, une question à la fois, pour écrire le CLAUDE.md du projet : ce que fait l'application, sa structure, les commandes, et les règles de travail. Les règles que je veux : une demande = un ticket = une branche ticket/<identifiant>-<mot-cle> ; avant de corriger une anomalie, un test qui la reproduit ; ne jamais modifier un test existant pour le faire passer ; pas de nouvelle dépendance sans demander ; commits en français avec l'identifiant du ticket ; Claude ne fusionne jamais. Montre-moi le fichier avant de l'écrire. »

**À observer** : les questions que Claude pose (ce qu'il ne peut pas deviner en lisant le code).
`CLAUDE.md` doit rester court : moins de 200 lignes, des règles qu'on peut vérifier.

## Étape 2 - Le hook qui relance les tests (15 min)

> « Écris un hook PostToolUse en Python, .claude/hooks/lancer_tests.py, qui relance uv run pytest à la racine du dépôt après chaque modification d'un fichier .py (sauf dans .venv), renvoie à Claude une ligne de résumé si tout passe, et l'extrait des échecs avec le code de sortie 2 sinon. Branche-le dans .claude/settings.json. Explique-moi chaque partie du fichier. »

Puis tapez `/hooks` pour vérifier qu'il est chargé (il faut parfois relancer `claude`). Et :

> « Ajoute un commentaire en haut de app/stock.py. »

**À observer** : la ligne « tests relancés automatiquement : 4 passed ». C'est votre pipeline sur le poste.

## Étape 3 - Le garde-fou (10 min)

> « Écris un hook PreToolUse, .claude/hooks/garde_fou.py, qui refuse rm -rf et ses variantes, toute poussée forcée (--force, -f, -uf, +branche), toute poussée sur main (nommée, ou un simple git push depuis main), et la lecture des fichiers .env. Fais court : moins de 100 lignes, que je puisse le relire. Branche-le, puis écris un petit script de test qui envoie au hook des exemples permis et interdits et vérifie la réponse. Lance-le. »

Puis la vraie tentative :

> « Lance exactement cette commande, je veux voir le garde-fou : rm -rf dossier-vide »

## Étape 4 - Le relecteur et la skill (15 min)

> « Crée le sous-agent .claude/agents/relecteur.md : il relit une branche comme une merge request (ticket, justesse, tests, simplicité, secrets) ; il signale comme bloquante toute modification d'un test existant ; il ne modifie rien et rend un verdict. »

> « Crée la skill .claude/skills/ticket-vers-merge-request/SKILL.md : lire le ticket, partir de main propre, créer la branche, proposer un plan et attendre mon accord, coder avec des tests, lancer tous les tests, commiter, faire relire par le relecteur, puis écrire la description de merge request dans merge-requests/<identifiant>.md (ajoute ce dossier au .gitignore). Elle ne fusionne jamais. »

Tapez `/agents` et `/` pour vérifier.

## Étape 5 - La chaîne sur un vrai ticket (10 min)

> « /ticket-vers-merge-request tickets/A-201-filtre-boutique.md »

**À observer** : le plan attendu avant le code, le hook après chaque fichier, le relecteur, la description
de merge request. Si une brique manque ou se comporte mal, corrigez-la : c'est le but de l'exercice.

Si vous avez le temps : traitez aussi le retour de recette `tickets/A-202-recette-seuil.md` (test qui échoue d'abord).

## Étape 6 - Comparer au modèle et préparer lundi (5 min, en autonomie)

Ouvrez `modeles/factory/` dans le kit (`LISEZMOI.md` d'abord). C'est la version générique de la même chaîne.
Ce dossier est hors du dépôt d'atelier : donnez-y d'abord accès à Claude en tapant
`/add-dir <chemin du kit>/modeles/factory`.

> « Compare mes fichiers .claude/ et CLAUDE.md à ceux du dossier <chemin du kit>/modeles/factory : qu'est-ce que le modèle fait et pas moi, et l'inverse ? Ne modifie rien. »

Notez dans `notes-lundi.md` (dans le dépôt d'atelier) : ce que vous copiez tel quel, ce que vous adaptez
(commande de tests, chemins, règles), et ce que vous devez demander (voir `modeles/factory/REGLAGES-GITLAB.md`).

## Comment vérifier

- `/hooks` montre un PreToolUse et un PostToolUse ; `/agents` montre `relecteur` ; `/` montre votre skill.
- Le garde-fou a refusé `rm -rf`, avec votre message.
- `git log --oneline --all` montre la branche `ticket/A-201-...` avec des commits clairs ; `main` n'a pas changé
  depuis l'ajout des fichiers de la chaîne.
- `uv run pytest` passe sur la branche, et `merge-requests/A-201.md` reprend chaque critère avec son test.

## Pour aller plus loin

- Ajoutez une skill `/recette` pour les anomalies, sur le modèle de `modeles/factory/claude/skills/recette/`.
- Écrivez deux vrais tickets de votre portail au format de `tickets/A-201` : « Interroge-moi jusqu'à
  pouvoir écrire ce ticket, avec des critères d'acceptation numérotés et vérifiables. »
