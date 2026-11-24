# Démonstration 3 : l'usine logicielle (15 min)

Ce qu'on voit : un ticket passe par tout le cycle avec les skills du kit : /start-dev, le développement,
/test-dev, /sync-dev, /verify, /ship-dev, la fusion par la personne qui relit, /close-dev.
Claude ne fusionne jamais : c'est la décision de la personne qui relit.

Le ticket : `projets/portail/tickets/T-100-accueil-traduction-compteur.md`. Il ajoute une carte sur la page
d'accueil du portail et affiche le nombre d'applications. Quatre critères.

Ce qui remplace GitLab et Jira dans le kit :

| Dans l'entreprise | Dans le kit |
|---|---|
| Le dépôt sur GitLab | un dépôt distant simulé dans `.depot-distant/`, créé par `/start-dev` la première fois |
| La merge request | le fichier `.depot-distant/merge-requests/T-100.md` (`uv run python outils/merge_request.py`) |
| Le tableau Jira | le fichier `.depot-distant/tableau-tickets.md` (`uv run python outils/tableau.py`) |
| Le bouton « Merge » | `! uv run python outils/merge_request.py fusionner T-100`, tapé par vous |

## 0. Les règles de l'équipe

Ouvrez `agents-docs/conventions/git.md` et `gitlab.md`. Ce sont les règles que les skills lisent avant d'agir :
nom des branches, format des commits, merge request en brouillon dès le début. Dans votre dépôt, `/setup-agents-doc`
les écrit en lisant le dépôt et en vous posant quelques questions.

## 1. Démarrer

> /start-dev T-100

À voir : les conventions lues, le résumé du ticket et ses 4 critères, la branche `ticket/T-100-accueil-traduction`,
le dossier `.worktrees/T-100` (une copie de travail à part), les tests au départ (12 réussis), la branche
envoyée, la merge request ouverte **en brouillon**, et le ticket passé « En cours ».

## 2. Faire le travail

> /plan

> « Traite le ticket T-100. Présente d'abord ton plan. »

Lisez le plan, puis validez-le. À voir : après chaque modification d'un fichier Python, la ligne du hook
« tests de projets/portail relancés automatiquement : ... passed ».

## 3. Tester

> /test-dev

À voir : chaque critère du ticket avec le test qui le prouve, puis tous les tests du portail.

## 4. Envoyer son travail, alors qu'un collègue a fusionné entre-temps

> « Lance outils/simuler_collegue.py »

Puis :

> /sync-dev

À voir : votre travail enregistré par un commit, la modification du collègue récupérée (« Olivier (collègue
simulé) »), les tests relancés, la branche envoyée, la merge request mise à jour (ce qui change, critères et
tests). Elle reste en brouillon.

## 5. Voir le résultat

> /verify

À voir : Claude lance le portail, ouvre la page d'accueil et regarde la nouvelle carte et le compteur. Cette
skill est fournie avec Claude Code. Si elle n'existe pas dans votre version, demandez : « Démarre le portail
depuis .worktrees/T-100, ouvre l'accueil et dis-moi ce que tu vois. » Puis « Arrête le portail ».

## 6. Envoyer en relecture

> /ship-dev

À voir : l'avis du sous-agent `relecteur`, la merge request terminée et passée « Prête à relire », le ticket
passé « En relecture ». Ouvrez `.depot-distant/merge-requests/T-100.md` : chaque critère du ticket a-t-il le
test qui le prouve ? Sur GitHub, le /ship d'Anthropic fait cette étape. Il n'est pas annoncé pour GitLab :
/ship-dev le remplace.

## 7. Fusionner, comme la personne qui relit

Tapez vous-même, précédé de « ! » (la commande part sans passer par Claude) :

> ! uv run python outils/merge_request.py fusionner T-100

Sur GitLab, c'est le bouton « Merge » de la merge request. Comme GitLab, la commande refuse un brouillon et
une branche en conflit avec main. Si vous demandez à Claude de fusionner, un hook le refuse.

## 8. Faire le ménage

> /close-dev T-100

À voir : Claude vérifie que la merge request est fusionnée et que la branche est bien dans `main` sur le dépôt
distant, supprime le worktree et la branche, met `main` à jour sur le poste, et passe le ticket « Terminé ».

## Pour aller plus loin

La version longue de cette démonstration : [l'exercice 02](../exercices/02-software-factory.md) (17 min en binôme, puis 1 h) : le ticket T-101, un retour de recette, une fusion avec conflit, un test piège. Pour Maxime ensuite : les exercices 07 et 08.

## Dans votre cas

| Qui | Cas | Le ticket | Ce que vérifient les tests |
|---|---|---|---|
| Maxime | Portail intranet | chaque demande ou retour de recette du portail | les pages et l'API répondent comme le ticket le demande |
| Maxime | Délais ORLI | « Mettre de côté les délais qui reculent de plus de 30 jours » | sur un petit Excel d'essai, la liste des changements attendue |
| Maxime | Visuels produits | « Recadrer les photos au format du site » | la taille des images produites, le nom des fichiers |
| Olivier | Traduction | « Ajouter le néerlandais de Belgique » | chaque terme du glossaire est bien traduit dans un texte d'essai |
| Olivier | Prévision des commandes web | « Ajouter une série pour les encombrants » | l'erreur ne se dégrade pas par rapport à la version d'avant |
| Augustin | Churn | « Recalculer les scores du mois » | le nombre de clients notés, aucune variable postérieure à la date |
| Céline | Analyses BigQuery | une demande d'analyse | le total retombe sur un chiffre connu |
