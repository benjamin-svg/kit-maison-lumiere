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

**Dans Claude Code Desktop** (l'application de bureau Claude, partie Code) : ouvrez une nouvelle session
et choisissez le dossier du kit comme dossier de travail. Le même `CLAUDE.md` et le même dossier `.claude/`
sont pris en compte. Desktop est plus confortable pour relire les modifications proposées (vue des
différences) ; le terminal est plus direct pour enchaîner les commandes. Les exercices marchent avec les deux.

Dans les deux cas, commencez par vous présenter : « Je suis Céline » (Claude utilisera `travail/celine/`).

## Ce que contient le kit

| Dossier ou fichier | Rôle |
|---|---|
| `CLAUDE.md` | Les consignes que Claude lit à chaque session : contexte, règles, commandes |
| `GLOSSAIRE.md` | Les mots techniques du kit, avec un exemple |
| `PRATIQUES.md` | Les pratiques de chaque métier sur lesquelles reposent les skills et les sous-agents |
| `donnees/` | Le script de génération, la base `ecommerce.duckdb` et les CSV de `brutes/` (lecture seule) |
| `semantique/` | La couche sémantique, volontairement incomplète : fiches des tables, métriques |
| `outils/` | `requete.py` (SQL en lecture seule), `tester_hooks.py` (contrôle des garde-fous) |
| `projets/portail/` | Petite application d'intranet (FastAPI), ses tests et ses tickets |
| `exercices/` | Les consignes des exercices (pour vous : Claude n'a pas le droit de les lire) |
| `modeles/` | Points de départ à copier hors du kit : dépôt d'atelier, usine logicielle, BigQuery |
| `lundi/` | Refaire le travail sur les vraies données : BigQuery, GitLab, prévision et churn, questions à poser |
| `travail/` | Un sous-dossier par participant, créé au fil des exercices (non versionné) |
| `.claude/` | Réglages et hooks, sous-agents (`agents/`), skills (`skills/`) |

## Plan des exercices

| N° | Exercice | Durée | Pour qui |
|---|---|---|---|
| 00 | [Prise en main](exercices/00-prise-en-main.md) | 30 min en salle (+ 20 min en autonomie) | tous |
| 01 | [Git en local](exercices/01-git.md) | 15 min en salle (+ 25 min en autonomie) | tous |
| 02 | [Du ticket à la merge request](exercices/02-software-factory.md) | 1 h (démonstration de 10 min pour tous) | Maxime |
| 03 | [Couche sémantique](exercices/03-couche-semantique.md) | 1 h | Céline |
| 04 | [Prévision des commandes web](exercices/04-ml-prevision.md) | 1 h | Olivier |
| 05 | [Churn](exercices/05-ml-churn.md) | 1 h | Augustin |
| 06 | [Cas d'analyse complet](exercices/06-cas-analyse.md) | 1 h 20 | Céline |
| 07 | [Construire son usine logicielle](exercices/07-construire-sa-factory.md) | 1 h | Maxime |
| 08 | [La chaîne sur un vrai GitLab](exercices/08-gitlab-pour-de-vrai.md) | 1 h | Maxime |

Le tronc commun dure 2 h 45, exercices compris : Claude Code et Desktop (1 h 10, avec l'exercice 00),
Git et GitLab (50 min, avec l'exercice 01), usine logicielle (45 min, avec la démonstration de l'exercice 02).

Les 3 h 15 de parcours, après le tronc commun (les étapes « en autonomie » de chaque fiche se font après la séance) :

| Qui | Déroulé |
|---|---|
| Maxime | 02 (1 h), 07 (1 h), 08 (1 h), bilan (15 min) |
| Céline | Couche sémantique : présentation (55 min) et 03 (1 h), puis 06 (1 h 20) |
| Olivier | Couche sémantique : présentation (55 min), méthode ML (1 h 05), 04 (1 h), bilan (15 min) |
| Augustin | Couche sémantique : présentation (55 min), méthode ML (1 h 05), 05 (1 h), bilan (15 min) |

Chaque consigne donne l'objectif, la durée, le texte exact à donner à Claude, ce qu'il faut observer,
comment vérifier le résultat (avec les chiffres ou les ordres de grandeur attendus), et une piste pour aller
plus loin. Chaque parcours se termine par la fiche `lundi/` qui le concerne.

## Les données en bref

- 400 produits (robes, chemises, pulls, pantalons, vestes, enfant, maison, accessoires), dont quelques
  articles **encombrants** (mobilier, tapis, mobilier enfant).
- Environ 20 000 clients, dont une partie anonymisée après deux ans d'inactivité.
- Environ 95 000 commandes et 210 000 lignes de commande du 1er janvier 2023 au 31 décembre 2025, sur trois
  canaux (`WEB`, `MAGASIN`, `MARKETPLACE`), avec soldes, Black Friday, ventes privées, retours et annulations.
- Les envois d'e-mails (ouvertures, clics), le calendrier commercial (dates réalisées), le plan commercial
  (chaque version publiée, plan 2026 compris), un agrégat quotidien `commandes_jour`, et une photo des clients
  au 30 juin 2025 pour le churn (`clients_churn_snapshot`).

Les données contiennent volontairement quelques pièges, comme dans la vraie vie. Les exercices aident à les trouver.

## Pour le formateur

- **Le corrigé n'est pas dans le kit** : il est à côté, dans `../formateur/corrige-formateur.md`, avec les
  chiffres de référence. L'historique git du kit ne l'a jamais contenu : vous pouvez distribuer le dossier du
  kit tel quel (copie ou archive), avec son dossier `.git`. Vérification : `git log --all --oneline -- '*corrige*'`
  ne renvoie rien.
- Claude n'a pas le droit de lire `exercices/` ni le script de génération (`.claude/settings.json` et hook) :
  sinon il annonce les pièges avant que le participant les cherche.
- Si vous modifiez le script de génération, les chiffres du corrigé ne sont plus valables.
- Le dossier est un dépôt git avec un premier commit : il sert de point de départ à l'exercice 01.
- **À préparer avant la séance** :
  - pour Maxime (exercice 08) : un compte gitlab.com vérifié (la vérification d'identité peut demander un
    téléphone), `glab` installé et connecté (`glab auth login`) ;
  - pour tous : `claude --version` (les slides citent la version 2.1.283 pour le mode Auto par défaut) ;
  - pour tous : un nom et une adresse pour les commits, sinon git refuse de commiter
    (`git config --global user.name "Prénom Nom"` et `git config --global user.email "adresse"`) ;
  - avant lundi : envoyer `lundi/a-demander.md` aux personnes concernées dans l'entreprise.
