---
name: setup-agents-doc
description: Crée ou met à jour le dossier agents-docs/conventions/ d'un dépôt - un fichier par sujet (git, gitlab, tests, jira) qui décrit les règles de l'équipe, trouvées dans le dépôt puis complétées par des questions. Les skills du cycle d'un ticket (/start-dev, /test-dev, /sync-dev, /ship-dev, /close-dev) lisent ces fichiers avant d'agir. À lancer une fois par dépôt, puis quand une règle change.
argument-hint: "[sujet à créer ou mettre à jour, facultatif : git, gitlab, tests, jira]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git status*), Bash(git log*), Bash(git branch*), Bash(git remote*), Bash(git symbolic-ref*), Bash(git config --get*), Bash(git rev-parse*), Bash(git add agents-docs*), Bash(git add CLAUDE.md), Bash(git commit*), Bash(ls *)
---

# Écrire les conventions de l'équipe pour les agents

Sujet : $ARGUMENTS (facultatif). Sans sujet, traiter les quatre : git, gitlab, tests, jira.

Pourquoi cette skill : un agent applique les règles qu'on lui donne. Si elles ne sont écrites nulle part, il
en invente : un nom de branche, un format de commit, un titre de merge request différents à chaque fois.
Écrites une fois dans `agents-docs/conventions/`, elles sont lues par chaque skill au moment où elle en a
besoin, et l'équipe les relit et les corrige comme du code.

Ce dossier ne remplace pas `CLAUDE.md` : `CLAUDE.md` décrit le dépôt (structure, commandes, règles
générales) et il est lu à chaque session. Les conventions décrivent une façon de travailler, et elles ne sont
lues que par les skills qui en ont besoin.

## Étapes

1. **Regarder ce qui existe** : `agents-docs/README.md` et `agents-docs/conventions/*.md`.
   - Ils existent : les lire, et pour chaque sujet comparer avec ce que montre le dépôt (étape 2). Proposer
     seulement les changements, un par un, avec la raison. Ne rien réécrire sans accord.
   - Ils n'existent pas : les créer (étapes 2 à 5).
2. **Trouver les règles déjà appliquées dans le dépôt**, sujet par sujet. Noter pour chaque règle d'où elle
   vient (fichier, ou commande et exemple).
   - **git** : branche principale (`git symbolic-ref refs/remotes/origin/HEAD`, sinon `main`), noms des
     branches (`git branch -a`), forme des messages (`git log --format="%s" -30`), fusions ou rebase
     (`git log --merges --oneline -10`), fichiers ignorés (`.gitignore`).
   - **gitlab** : adresse du dépôt (`git remote -v`), `.gitlab-ci.yml` (ce que vérifie la CI),
     `.gitlab/merge_request_templates/`, `CODEOWNERS`, `CONTRIBUTING.md`.
   - **tests** : outil et configuration (`pytest.ini`, `pyproject.toml`, `conftest.py`), dossiers `tests/`,
     commande qui les lance (README, `CLAUDE.md`, CI), forme des noms de tests existants.
   - **jira** : forme des identifiants dans les branches et les commits (`ECOM-123`, `T-101`), dossiers de
     tickets, colonnes du tableau si elles sont décrites quelque part.
3. **Poser les questions qui restent**, une à la fois, en proposant la réponse la plus probable. Au plus
   cinq questions en tout. Exemples : « Qui fusionne les merge requests ? », « Fusion avec un commit de
   fusion ou en squash ? », « Une merge request s'ouvre-t-elle en brouillon dès le début du ticket ? ».
   Ce que la personne ne sait pas : l'écrire comme « à confirmer avec l'équipe », sans l'inventer.
4. **Écrire les fichiers** `agents-docs/conventions/<sujet>.md` :
   - des règles courtes, à l'impératif ou au présent, regroupées par moment (branches, commits, merge request,
     fusion...) ;
   - un exemple réel pour chaque règle de nommage (un nom de branche, un message de commit, un titre) ;
   - le pourquoi en une phrase quand la règle n'est pas évidente ;
   - une partie « Dans ce dépôt » pour les commandes propres au dépôt (outil de tickets, commande `glab`) ;
   - moins de 60 lignes par fichier : un agent les lit avant chaque action.
   Puis `agents-docs/README.md` : à quoi sert le dossier, et un tableau fichier, sujet, skills qui le lisent.
5. **Ajouter un renvoi dans `CLAUDE.md`**, une ligne, sans recopier les règles : « Conventions de l'équipe
   (git, GitLab, tests, tickets) : `agents-docs/conventions/`. À lire avant toute action sur une branche, un
   test, une merge request ou un ticket. » S'il existe déjà, ne rien ajouter.
6. **Faire relire, puis enregistrer** : montrer la liste des fichiers et les règles marquées « à confirmer ».
   Avec l'accord de la personne : `git add agents-docs CLAUDE.md`, puis
   `git commit -m "Ajoute les conventions de l'équipe pour les agents"`. Ne pas envoyer (pas de push) : ces
   règles concernent toute l'équipe, elles passent par une merge request comme le reste.

## Ce que tu affiches à la fin

```
Conventions écrites dans agents-docs/conventions/ :
✓ git.md : <n> règles (<la plus importante>)
✓ gitlab.md : <n> règles
✓ tests.md : <n> règles
✓ jira.md : <n> règles
À confirmer avec l'équipe : <liste, ou « rien »>
✓ Renvoi ajouté dans CLAUDE.md
✓ Commit : <message, ou « pas encore, en attente de ton accord »>
```

Puis : « /start-dev, /test-dev, /sync-dev, /ship-dev et /close-dev suivront ces règles. Pour les partager,
envoie-les à l'équipe par une merge request. »

Ne modifie aucun autre fichier que `agents-docs/` et la ligne de renvoi de `CLAUDE.md`.
