# Réglages GitLab du premier jour

À faire une fois par projet, par une personne qui a le rôle **Maintainer** (ou Owner).
Les noms de menus sont ceux de GitLab en anglais (l'interface en français les traduit).

## 1. Protéger la branche principale

**Settings > Repository > Protected branches** (ou **Branch rules** selon la version).

- `main` : « Allowed to push and merge » = **No one** pour le push, **Maintainers** pour le merge.
- « Allowed to force push » : désactivé.

Effet : personne ne pousse directement sur `main` ; tout passe par une merge request.

## 2. Bloquer la fusion tant que le pipeline n'est pas vert

**Settings > Merge requests > Merge checks** :

- cocher **Pipelines must succeed** ;
- cocher **All threads must be resolved** (un commentaire non traité bloque la fusion).

Ces deux réglages existent dans l'offre gratuite.

## 3. Rendre la relecture obligatoire

**Settings > Merge requests > Merge request approvals** : au moins **1 approbation**, et « Prevent approval
by author » (l'auteur ne s'approuve pas lui-même).

**Attention** : les règles d'approbation obligatoires demandent l'offre **Premium** ou **Ultimate**.
En offre gratuite, on peut demander une approbation, mais pas l'exiger. À vérifier avant lundi :
quelle offre a le GitLab de l'entreprise ? Sans Premium, la règle « une relecture avant fusion » est une
règle d'équipe, écrite dans `CLAUDE.md` et tenue par les personnes qui ont le droit de fusionner.

## 4. Le modèle de merge request

Le fichier `.gitlab/merge_request_templates/Default.md` est proposé automatiquement à chaque nouvelle
merge request (sur gitlab.com ; sur une instance de l'entreprise, vérifier qu'il apparaît).

## 5. Les secrets du pipeline

**Settings > CI/CD > Variables** : une variable par secret (par exemple les droits d'accès à BigQuery
d'un compte de service), cochée **Masked** (cachée dans les journaux) et **Protected** (seulement sur les
branches protégées). Jamais de secret dans `.gitlab-ci.yml` ni dans le dépôt.

## 6. Le pipeline planifié

**Build > Pipeline schedules > New schedule** : description, intervalle (`0 6 * * 1` = chaque lundi à 6 h),
fuseau **Europe/Paris**, branche `main`. Seuls les jobs avec la règle `$CI_PIPELINE_SOURCE == "schedule"`
tournent (voir le job `traitement-planifie` de `gitlab-ci.yml`).

Le planning tourne avec les droits de la personne qui l'a créé : si elle quitte le projet, il s'arrête.
Prévoir qui le reprend.

## 7. Ce qu'il faut demander à l'administrateur GitLab

- L'offre (Free, Premium, Ultimate).
- Les runners : partagés ou propres au groupe ? Acceptent-ils une image Docker publique ? Ont-ils accès à
  PyPI ou à un miroir interne ?
- Le droit d'utiliser `glab` avec un jeton personnel (droits `api`, durée), et qui le délivre.
