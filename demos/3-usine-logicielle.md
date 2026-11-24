# Démonstration 3 : l'usine logicielle (15 min)

Ce qu'on voit : un ticket passe par tout le cycle avec les trois skills du kit, de la branche à la merge
request. Claude ne fusionne jamais : c'est la décision de la personne qui relit.

Le ticket : `projets/portail/tickets/T-100-accueil-traduction-compteur.md`. Il ajoute une carte sur la page
d'accueil du portail et affiche le nombre d'applications. Quatre critères.

Ce qui remplace GitLab dans le kit : un dépôt distant simulé dans `.depot-distant/`, créé par `/start-dev`
la première fois. La merge request est un fichier : `travail/<prénom>/merge-requests/T-100.md`.

## 1. Démarrer

> /start-dev T-100

À voir : le résumé du ticket et ses 4 critères, la branche `ticket/T-100-accueil-traduction`, le dossier
`.worktrees/T-100` (une copie de travail à part), et les tests au départ (12 réussis).

## 2. Faire le travail

> « Traite le ticket T-100. Présente d'abord ton plan. »

Lisez le plan, puis validez-le. À voir : après chaque modification d'un fichier Python, la ligne du hook
« tests de projets/portail relancés automatiquement : ... passed ». Le nombre de tests augmente.

## 3. Un collègue a fusionné entre-temps

> « Lance outils/simuler_collegue.py »

Puis :

> /sync-dev

À voir : votre travail enregistré par un commit, la modification du collègue récupérée (« Olivier (collègue
simulé) »), les tests relancés, la branche envoyée sur le dépôt distant.

## 4. Terminer

> /close-dev

À voir : les tests, l'avis du sous-agent `relecteur`, le dernier commit avec « T-100 », la branche envoyée,
et la merge request écrite dans `travail/<prénom>/merge-requests/T-100.md`. Ouvrez-la : chaque critère du
ticket a-t-il le test qui le prouve ?

Pour voir le résultat : « Démarre le portail depuis .worktrees/T-100 et donne-moi l'adresse. » Puis
« Arrête le portail ».

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
