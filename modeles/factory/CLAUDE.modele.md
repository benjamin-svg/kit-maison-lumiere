# <Nom du projet>

<Une phrase : ce que fait l'application, et pour qui.>

## Structure

- `<dossier>/` : <rôle>
- `tests/` : tests automatisés
- `tickets/` : les demandes à traiter (si les tickets ne sont pas dans GitLab)

## Commandes

- Installer : `<commande>`
- Tests : `<commande>` (le hook la relance après chaque modification de code)
- Lancer l'application : `<commande>` puis ouvrir <adresse>

## Règles pour ce projet

- Une demande = un ticket = une branche `ticket/<identifiant>-<mot-cle>`. Jamais de commit direct sur `main`.
- Avant de corriger une anomalie, écrire un test qui la reproduit et vérifier qu'il échoue.
- Ne jamais modifier un test existant pour le faire passer : si un test semble faux, le signaler et demander.
- Pas de nouvelle dépendance sans le demander.
- Aucun secret (mot de passe, jeton, clé) ni donnée personnelle dans le dépôt.
- Messages de commit en français, au présent, avec l'identifiant du ticket : « Ajoute le filtre boutique (A-201) ».
- La fusion dans `main` se fait par une merge request relue, avec un pipeline vert. Claude ne fusionne pas.
- Tutoyer la personne ; expliquer en français simple.
