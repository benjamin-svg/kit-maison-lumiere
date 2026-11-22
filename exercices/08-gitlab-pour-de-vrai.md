# Exercice 08 - La chaîne sur un vrai GitLab (gitlab.com)

## Objectif

Pousser le dépôt d'atelier de l'exercice 07 sur gitlab.com, et vivre le cycle complet : branche, merge request
ouverte par Claude, pipeline qui teste, pipeline rouge qui bloque la fusion, commentaire de relecture traité par
Claude, fusion après un pipeline vert, puis pipeline planifié. C'est le même cycle que sur le GitLab de l'entreprise.

## Durée

1 heure (parcours de Maxime).

## À préparer avant la séance (avec le formateur)

- Un compte gitlab.com personnel. GitLab peut demander une vérification d'identité (téléphone, parfois carte
  bancaire) avant le premier pipeline : à faire **avant** la séance.
- `glab`, l'outil officiel de GitLab en ligne de commande, installé et connecté : `glab auth login`.
- Le dépôt `~/atelier-factory` de l'exercice 07. Si vous ne l'avez pas fini, copiez `modeles/depot-atelier/`
  et les fichiers de `modeles/factory/` (voir son `LISEZMOI.md`).

**Si gitlab.com n'est pas accessible** (réseau, compte non vérifié), un dossier local joue le rôle du serveur :

```bash
git init --bare ~/serveur-atelier.git     # le « serveur » : un dépôt sans fichiers de travail
```

- Étape 1 : donnez ce chemin à la place de l'adresse GitLab. Les poussées et le garde-fou marchent pour de vrai.
- Étape 2 : faites créer la branche, le `.gitlab-ci.yml` et le modèle de merge request, poussez, mais sans `glab`.
  Aucun pipeline ne se lance tout seul : lancez à la main ce que ferait le runner, en demandant à Claude
  « Lis .gitlab-ci.yml et lance, dans l'ordre, les commandes du job tests, comme le ferait le runner. »
- Étape 4 : faites-la en local ; la première barrière (le hook qui relance les tests) est bien réelle.
- Étapes 3, 5 et 6 : lisez-les avec Claude, `REGLAGES-GITLAB.md` sous les yeux : « Explique-moi, sans rien
  exécuter, ce que ferait cette étape et ce que je verrais dans GitLab. » Le formateur montre les écrans.

## Étape 1 - Créer le projet et pousser (10 min)

Sur gitlab.com : **New project > Create blank project**, nom `atelier-factory`, visibilité **Private**,
sans fichier README. Puis, dans Claude, depuis `~/atelier-factory` :

> « Relie ce dépôt à mon projet GitLab atelier-factory (adresse : <collez l'adresse du projet>) et pousse main. Montre-moi les commandes avant de les lancer. »

**À observer** : `git remote add origin ...` puis `git push -u origin main`. La poussée sur `main` est permise
cette fois seulement : le projet est vide. Si votre garde-fou la refuse, c'est qu'il marche : faites-la vous-même
dans le terminal.

## Étape 2 - Le pipeline (10 min)

> « Crée une branche ticket/A-210-pipeline (pas de ticket écrit pour celle-ci : c'est l'installation du pipeline). Ajoute un .gitlab-ci.yml qui installe le projet avec uv et lance les tests à chaque merge request et sur main, en t'inspirant de <chemin du kit>/modeles/factory/gitlab-ci.yml. Ajoute aussi .gitlab/merge_request_templates/Default.md depuis le même dossier. Garde le job traitement-planifie, il servira à l'étape 6. Commite, pousse la branche, et ouvre une merge request vers main avec glab, en brouillon. Puis suis le pipeline avec glab ci status et dis-moi quand il est fini. »

**À observer** : dans GitLab, **Build > Pipelines** : le pipeline se lance seul. Dans la merge request,
l'onglet des tests affiche le détail (rapport JUnit).

## Étape 3 - Les réglages de protection (10 min)

Dans GitLab, avec `modeles/factory/REGLAGES-GITLAB.md` sous les yeux :

- **Settings > Repository > Protected branches** : `main`, push « No one », merge « Maintainers ».
- **Settings > Merge requests > Merge checks** : cocher **Pipelines must succeed** et **All threads must be resolved**.

Notez ce qui n'est pas disponible en offre gratuite (approbations obligatoires).

## Étape 4 - Un pipeline rouge bloque la fusion (10 min)

> « Sur la branche ticket/A-210-pipeline, modifie app/stock.py pour que la règle de réapprovisionnement soit fausse (stock supérieur au seuil). Je veux voir un pipeline rouge. Commite et pousse, sans lancer les tests en local. »

Votre hook relancera quand même les tests sur le poste et les verra échouer : c'est la première barrière.
Dans GitLab, le pipeline est rouge et le bouton **Merge** est bloqué : c'est la seconde.

> « Annule ce dernier commit avec git revert, pousse, et attends le pipeline vert. »

## Étape 5 - Un commentaire de relecture traité par Claude (10 min)

Dans GitLab, onglet **Changes** de la merge request : commentez une ligne du `.gitlab-ci.yml`, par exemple
« Ajoute un commentaire en français au-dessus de chaque job pour dire à quoi il sert. »

> « Lis les commentaires non résolus de ma merge request avec glab, fais les corrections, pousse, et réponds à chaque commentaire pour dire ce qui a été fait. »

**À observer** : `glab mr view <n> --comments`, la correction, la réponse de Claude dans le fil.
Marquez vous-même le fil comme résolu : c'est une décision de relecteur.

## Étape 6 - Fusionner, puis planifier (10 min)

Relisez le diff complet dans GitLab, retirez le statut brouillon, puis fusionnez **vous-même** avec le bouton
**Merge** (ou demandez à Claude la commande `glab mr merge`, et lancez-la vous-même).

Puis **Build > Pipeline schedules > New schedule** : « Contrôle du lundi », intervalle `0 6 * * 1`,
fuseau Europe/Paris, branche `main`. Cliquez sur **Run** (le bouton de lecture) pour le lancer tout de suite.

**À observer** : seul le job `traitement-planifie` tourne. C'est ainsi que tournera chaque lundi un script
comme la prévision d'Olivier, **sans Claude** : la CI relance les scripts, pas l'agent.

## Comment vérifier

- Sur gitlab.com : `main` contient `.gitlab-ci.yml` ; la merge request est fusionnée ; son fil de commentaires
  montre la réponse de Claude ; un pipeline rouge puis un vert apparaissent dans **Build > Pipelines**.
- `main` est protégée et « Pipelines must succeed » est coché.
- Un pipeline planifié existe et a tourné une fois.

## Pour aller plus loin

- Faites traiter le ticket `tickets/A-202-recette-seuil.md` de bout en bout, jusqu'à la merge request sur GitLab.
- Ajoutez `Closes #1` dans la description d'une merge request, après avoir créé le ticket n° 1 avec
  `glab issue create` : le ticket se ferme à la fusion.
- Bilan (15 min) : complétez `notes-lundi.md` avec ce que vous devez demander à l'administrateur GitLab de
  l'entreprise (section 7 de `REGLAGES-GITLAB.md`).
