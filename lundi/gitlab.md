# Lundi sur GitLab : brancher la chaîne sur le dépôt de l'entreprise

## 1. La chaîne sur le poste

Les fichiers à copier et à adapter sont dans `modeles/factory/` : commencez par son `LISEZMOI.md`
(ce qu'on copie, ce qu'on adapte, comment vérifier). Les réglages du projet GitLab sont dans
`modeles/factory/REGLAGES-GITLAB.md`.

Ordre conseillé, sur un petit projet d'abord :
1. `CLAUDE.md` du projet (« Lis le dépôt et remplis CLAUDE.md ; pose-moi les questions »).
2. Le hook de tests (`COMMANDE_TESTS` à adapter), vérifié avec `/hooks` et une petite modification.
3. Le garde-fou, vérifié par une vraie tentative refusée.
4. Le relecteur et la skill `/ticket-vers-merge-request`, vérifiés sur un vrai petit ticket.
5. `glab auth login`, puis la première merge request ouverte par Claude, relue et fusionnée par un collègue.

## 2. Le pipeline (CI) : il relance les scripts, pas Claude

La CI de GitLab tourne **sans Claude** : les abonnements Claude sont liés aux personnes, et une clé d'API
facturée à l'usage serait une autre décision. Elle relance ce que Claude a aidé à écrire : les tests à chaque
merge request, et les traitements planifiés (prévision du lundi, liste churn du mois, contrôle des données).

Point de départ : `modeles/factory/gitlab-ci.yml`. Deux jobs : `tests` (merge request et `main`) et
`traitement-planifie` (pipeline planifié seulement).

## 3. Un traitement planifié qui lit BigQuery

Exemple pour la prévision du lundi (à adapter) :

```yaml
prevision-du-lundi:
  stage: planifie
  image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim
  script:
    - uv sync --frozen
    - uv run python prevoir_hebdo.py --date-origine "$(date +%F)"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

**L'accès à BigQuery depuis le pipeline** passe par un **compte de service** (une identité technique, pas une
personne), avec les seuls droits utiles. Deux façons, à choisir avec l'équipe qui gère Google Cloud :

- une clé du compte de service rangée dans une variable CI/CD **masquée et protégée**
  (Settings > CI/CD > Variables), jamais dans le dépôt ;
- mieux, la **fédération d'identité** : GitLab fournit au job un jeton (`id_tokens` dans `.gitlab-ci.yml`) que
  Google Cloud échange contre un accès temporaire, sans clé à stocker. Plus sûr, mais à configurer côté Google Cloud.

Si le job échoue, GitLab prévient par e-mail la personne qui a créé le planning. Prévoir qui la remplace.

## 4. Ce qui reste humain

- Relire le diff et fusionner : jamais Claude.
- Décider qu'un test existant était faux et peut être modifié.
- Approuver une merge request écrite avec l'aide de Claude par la même personne : un deuxième regard,
  même si l'offre GitLab ne l'impose pas (voir `REGLAGES-GITLAB.md`, section 3).
