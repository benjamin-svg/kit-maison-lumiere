# Modèle d'usine logicielle à copier dans un vrai dépôt

Ces fichiers sont la version **générique** de la chaîne du kit : ils ne dépendent ni du kit, ni de DuckDB,
ni des chemins `projets/<nom>/`. Ils servent de point de comparaison à l'exercice 07, et de point de départ
lundi, sur votre vrai dépôt.

Les dossiers sont nommés sans point (`claude/`, `gitlab/`) pour que Claude Code ne les charge pas quand
vous travaillez dans le kit. À la copie, ils prennent leur vrai nom.

## Ce qu'il faut copier, et où

| Fichier du modèle | Dans votre dépôt | Rôle |
|---|---|---|
| `CLAUDE.modele.md` | `CLAUDE.md` | Les règles du projet, lues à chaque session. À remplir. |
| `claude/settings.json` | `.claude/settings.json` | Permissions et branchement des hooks |
| `claude/hooks/lancer_tests.py` | `.claude/hooks/lancer_tests.py` | Relance les tests après chaque modification de code |
| `claude/hooks/garde_fou.py` | `.claude/hooks/garde_fou.py` | Refuse `rm -rf`, toute poussée forcée (`--force`, `-f`, `+branche`), toute poussée sur `main` (nommée ou depuis `main`), les fichiers de secrets |
| `tester_garde_fou.py` | (reste dans le kit) | Vérifie le garde-fou sans rien pousser : `python3 tester_garde_fou.py` |
| `claude/agents/relecteur.md` | `.claude/agents/relecteur.md` | Le sous-agent qui relit une branche |
| `claude/skills/ticket-vers-merge-request/` | `.claude/skills/ticket-vers-merge-request/` | Du ticket à la merge request (locale ou GitLab) |
| `claude/skills/recette/` | `.claude/skills/recette/` | Du retour de recette au test qui échoue |
| `gitlab-ci.yml` | `.gitlab-ci.yml` | Le pipeline : tests à chaque merge request, traitement planifié |
| `gitlab/merge_request_templates/Default.md` | `.gitlab/merge_request_templates/Default.md` | Le modèle de description de merge request |

Commande, depuis le dossier de votre dépôt (remplacez `<kit>` par le chemin du kit) :

```bash
mkdir -p .claude .gitlab
cp <kit>/modeles/factory/CLAUDE.modele.md CLAUDE.md
cp -r <kit>/modeles/factory/claude/. .claude/
cp -r <kit>/modeles/factory/gitlab/. .gitlab/
cp <kit>/modeles/factory/gitlab-ci.yml .gitlab-ci.yml
```

## Ce qu'il faut adapter

1. **`CLAUDE.md`** : structure, commandes, règles. Demandez à Claude : « Lis le dépôt et remplis CLAUDE.md ;
   pose-moi les questions pour ce que tu ne peux pas deviner. »
2. **`lancer_tests.py`** : les deux lignes `COMMANDE_TESTS` et `EXTENSIONS`, en haut du fichier.
   Projet JavaScript : `["npm", "test"]` et `{".js", ".ts"}`. Projet Java : `["mvn", "-q", "test"]` et `{".java"}`.
3. **`settings.json`** : les hooks sont lancés avec `python3`. Sous Windows, remplacez par `python` (ou `py`).
   Ajoutez aux permissions les commandes habituelles du projet.
4. **`garde_fou.py`** : ajoutez les règles propres au projet (dossier en lecture seule, commande coûteuse...).
   `BRANCHE_PRINCIPALE` si la vôtre ne s'appelle pas `main`.
   Après chaque changement, ajoutez un cas dans `tester_garde_fou.py` et relancez-le : tous les cas doivent être conformes.
5. **`.gitlab-ci.yml`** : l'image et les commandes du job `tests` ; le script du job `traitement-planifie`.
   Demandez à l'administrateur GitLab si les runners de l'entreprise acceptent une image Docker publique
   et ont accès à PyPI (sinon : miroir interne).

## Comment vérifier que tout est branché

1. Lancez `claude` dans le dépôt et acceptez la confiance au dossier.
2. `/hooks` : un hook PreToolUse et un hook PostToolUse. `/agents` : `relecteur`. `/` : vos deux skills.
3. « Lance exactement cette commande : rm -rf dossier-qui-n-existe-pas » : le garde-fou doit refuser.
4. Faites traiter un petit ticket avec `/ticket-vers-merge-request` : vous devez voir la ligne
   « Hook : tests relancés automatiquement : ... passed » après chaque modification.
5. Sur GitLab : le pipeline de la merge request passe au vert. Voir `REGLAGES-GITLAB.md`.

## Ce que le modèle ne fait pas

- Il ne lance pas Claude dans la CI : la CI relance vos scripts et vos tests, sans Claude
  (les abonnements Claude sont liés aux personnes).
- Il ne remplace pas la relecture humaine : la fusion reste la décision d'un collègue.
