# Kit de formation Claude Code - Maison Lumière

Ce kit sert à apprendre à travailler avec **Claude Code** sur des cas proches du quotidien d'une équipe
e-commerce : analyses SQL, couche sémantique, petite application web, prévision des commandes, churn
(la perte de clients).

Tout tourne **sur votre poste**, sans compte cloud ni clé d'API à configurer pour les données :
la marque **Maison Lumière** est fictive, et toutes les données sont générées par un script
(graine fixe : tout le monde a exactement les mêmes chiffres).

## Installation (3 commandes)

Prérequis : [uv](https://docs.astral.sh/uv/) et git installés ; Claude Code installé et connecté à votre compte.

```bash
cd kit                             # le dossier du kit (son nom peut varier)
uv sync                            # installe Python et les bibliothèques dans .venv/
uv run python donnees/generer_donnees.py   # génère la base DuckDB et les CSV (quelques secondes)
```

Pour vérifier que tout va bien :

```bash
cd projets/portail && uv run pytest -q && cd ../..   # tests du portail : tous verts
uv run python outils/tester_hooks.py                 # garde-fous : « Tous les cas sont conformes. »
```

## Ouvrir le kit dans Claude Code

**Dans un terminal** : se placer dans le dossier du kit, puis lancer `claude`.

```bash
cd kit
claude
```

Au premier lancement, Claude Code demande si vous faites confiance au dossier : répondez oui
(c'est ce qui active les réglages, les hooks, les skills et les sous-agents de `.claude/`).
Tapez `/` pour voir les commandes disponibles, dont les skills du kit.

**Dans Claude Desktop** (l'application de bureau Claude, onglet Code) : ouvrez une nouvelle session
et choisissez le dossier du kit comme dossier de travail. Le même `CLAUDE.md` et le même dossier `.claude/`
sont pris en compte. Desktop est plus confortable pour relire les modifications proposées (vue des
différences) ; le terminal est plus direct pour enchaîner les commandes. Les démonstrations marchent avec les deux.

Dans les deux cas, commencez par vous présenter : « Je suis <votre prénom> » (par exemple, pour Céline, Claude utilisera `travail/celine/`).

## Ce que contient le kit

| Dossier ou fichier | Rôle |
|---|---|
| `CLAUDE.md` | Les consignes que Claude lit à chaque session : contexte, règles, commandes |
| `GLOSSAIRE.md` | Les mots techniques du kit, avec un exemple |
| `PRATIQUES.md` | Les pratiques de chaque métier sur lesquelles reposent les skills et les sous-agents |
| `donnees/` | Le script de génération, la base `ecommerce.duckdb` et les CSV de `brutes/` (lecture seule) |
| `semantique/` | La couche sémantique, volontairement incomplète : fiches des tables, métriques |
| `outils/` | `requete.py` (SQL en lecture seule), `tester_hooks.py` (contrôle des garde-fous), `depot_distant.py` et `simuler_collegue.py` (démonstration 3) |
| `projets/portail/` | Petite application d'intranet (FastAPI), ses tests et ses tickets |
| `demos/` | Le parcours rapide : 5 démonstrations, une par partie, avec le lien vers votre cas d'usage |
| `exercices/` | Les exercices complets, 00 à 08 (pour vous : Claude n'a pas le droit de les lire) |
| `modeles/` | Les points de départ des exercices 07 et 08 : dépôt d'atelier, usine logicielle |
| `travail/` | Un sous-dossier par participant, créé au fil des démonstrations et des exercices (non versionné) |
| `.claude/` | Réglages et hooks, sous-agents (`agents/`), skills (`skills/`), règles par sujet (`rules/`) |

## Deux façons de pratiquer : le parcours rapide ou les exercices complets

Après chaque partie de la formation, chacun choisit :

- **le parcours rapide** : une démonstration de 8 à 15 minutes (`demos/`), pour voir une fois chaque élément
  fonctionner avec Claude, puis directement son propre cas d'usage.
- **les exercices complets** : les fiches de `exercices/`, plus longues, qui font tout pratiquer sur le kit
  avant de passer à son cas.

Les deux mènent au même endroit. Chaque démonstration se termine par un tableau « Dans votre cas », et
renvoie à l'exercice complet qui va plus loin sur le même sujet.

| Partie | Parcours rapide | Durée | Exercice complet | Durée |
|---|---|---|---|---|
| Claude Code | [Démonstration 1](demos/1-claude-code.md) | 8 min | [00 Prise en main](exercices/00-prise-en-main.md) | 30 min (+ 20 min) |
| Git | [Démonstration 2](demos/2-git.md) | 8 min | [01 Git avec Claude](exercices/01-git.md) | 15 min (+ 15 min) |
| Usine logicielle | [Démonstration 3](demos/3-usine-logicielle.md), ticket T-100 | 15 min | [02 Le cycle d'un ticket](exercices/02-software-factory.md), puis [07](exercices/07-construire-sa-factory.md) et [08](exercices/08-gitlab-pour-de-vrai.md) pour Maxime | 17 min, puis 3 h |
| Couche sémantique | [Démonstration 4](demos/4-couche-semantique.md) | 10 min | [03 Couche sémantique](exercices/03-couche-semantique.md), puis [06 Cas d'analyse](exercices/06-cas-analyse.md) | 1 h, puis 1 h 05 |
| Apprentissage automatique | [Démonstration 5](demos/5-modelisation.md), skill `/entrainer-modele` | 10 min | [04 Prévision](exercices/04-ml-prevision.md) ou [05 Churn](exercices/05-ml-churn.md) | 1 h |

Entre parenthèses : les étapes « en autonomie », à faire après la séance.

**Avec le parcours rapide**, le tronc commun dure 2 h 30 : Claude Code et Desktop (55 min), Git et GitLab
(45 min), usine logicielle (50 min). Puis, pendant les 3 h 30 de parcours :

| Qui | Déroulé |
|---|---|
| Maxime | Ses cas tout de suite : le portail, puis les délais ORLI ou les visuels s'il reste du temps. Bilan (15 min) |
| Céline | Couche sémantique (1 h 10), puis son cas : les fiches de ses tables et ses analyses (2 h 05). Bilan |
| Olivier | Couche sémantique (1 h 10), apprentissage automatique (1 h 20), puis la prévision (45 min). Bilan |
| Augustin | Couche sémantique (1 h 10), apprentissage automatique (1 h 20), puis le churn (45 min). Bilan |

**Avec les exercices complets**, le tronc commun dure 2 h 45, puis :

| Qui | Déroulé |
|---|---|
| Maxime | 02, étapes 6 à 9 (1 h), 07 (1 h), 08 (1 h), bilan (15 min) |
| Céline | Couche sémantique : présentation (55 min) et 03 (1 h), puis 06 (1 h 05), bilan (15 min) |
| Olivier | Couche sémantique : présentation (55 min), apprentissage automatique (1 h 05), 04 (1 h), bilan (15 min) |
| Augustin | Couche sémantique : présentation (55 min), apprentissage automatique (1 h 05), 05 (1 h), bilan (15 min) |

On peut mélanger : par exemple le parcours rapide pour Claude Code et Git, puis l'exercice complet de sa partie.
Chaque consigne d'exercice donne l'objectif, la durée, le texte exact à donner à Claude, ce qu'il faut observer,
comment vérifier le résultat, et une piste pour aller plus loin.

## Les données en bref

- 400 produits (robes, chemises, pulls, pantalons, vestes, enfant, maison, accessoires), dont quelques
  articles **encombrants** (mobilier, tapis, mobilier enfant).
- Environ 20 000 clients, dont une partie anonymisée après deux ans d'inactivité.
- Environ 95 000 commandes et 210 000 lignes de commande du 1er janvier 2023 au 31 décembre 2025, sur trois
  canaux (`WEB`, `MAGASIN`, `MARKETPLACE`), avec soldes, Black Friday, ventes privées, retours et annulations.
- Les envois d'e-mails (ouvertures, clics), le calendrier commercial (dates réalisées), le plan commercial
  (chaque version publiée, plan 2026 compris), un agrégat quotidien `commandes_jour`, et une photo des clients
  au 30 juin 2025 pour le churn (`clients_churn_snapshot`).

Les données contiennent volontairement quelques pièges, comme dans la vraie vie. La démonstration 4 en montre un, les exercices aident à trouver les autres.

## Pour le formateur

- **Le corrigé n'est pas dans le kit** : il est à côté, dans `../formateur/corrige-formateur.md`, avec les
  chiffres de référence. L'historique git du kit ne l'a jamais contenu : vous pouvez distribuer le dossier du
  kit tel quel (copie ou archive), avec son dossier `.git`. Vérification : `git log --all --oneline -- '*corrige*'`
  ne renvoie rien.
- Claude n'a pas le droit de lire `exercices/` ni le script de génération (`.claude/settings.json` et hook) :
  sinon il annonce les pièges avant que le participant les cherche.
- Si vous modifiez le script de génération, les chiffres du corrigé ne sont plus valables.
- Le dossier est un dépôt git avec un premier commit : il sert de point de départ à la démonstration 2 et à l'exercice 01.
- **À préparer avant la séance** :
  - pour Maxime (exercice 08) : un compte gitlab.com vérifié (la vérification d'identité peut demander un
    téléphone), `glab` installé et connecté (`glab auth login`) ;
  - pour tous : `claude --version` (les slides citent la version 2.1.283 pour le mode Auto par défaut) ;
  - pour tous : un nom et une adresse pour les commits, sinon git refuse de commiter
    (`git config --global user.name "Prénom Nom"` et `git config --global user.email "adresse"`) ;
  - pour la démonstration 3 et l'exercice 02 : rien à préparer, `/start-dev` crée le dépôt distant simulé la première fois.
    Si le kit a déjà un dépôt distant (`origin`, par exemple un vrai GitLab), faire la démonstration dans une
    copie tirée de l'archive : les scripts refusent de toucher à un vrai GitLab ;
  - pour les cas d'usage : demander à chacun d'apporter un extrait de ses vraies données ou de son vrai
    fichier (anonymisé si besoin), et de savoir où trouver son dépôt GitLab ;
