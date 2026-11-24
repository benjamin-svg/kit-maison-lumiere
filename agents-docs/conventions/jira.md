# Conventions des tickets (Jira)

## Le ticket

- Chaque demande a un ticket avant tout développement.
- Identifiant : `T-<numéro>` dans le kit (sur Jira, la clé du projet, par exemple `ECOM-123`).
  On le retrouve partout : nom de la branche, messages de commit, titre de la merge request.
- Un ticket prêt contient : le contexte, la demande, et des critères d'acceptation **numérotés et
  vérifiables**. Un critère flou se reformule avec le demandeur avant de coder.

## Le tableau

| Colonne | Quand | Qui la change |
|---|---|---|
| À faire | le ticket est prêt | le demandeur |
| En cours | la branche et la merge request en brouillon existent | /start-dev |
| En relecture | la merge request est prête à relire | /ship-dev |
| Terminé | la merge request est fusionnée et le poste est rangé | /close-dev |

## Dans le kit

- Les tickets sont des fichiers `projets/<projet>/tickets/T-<numéro>-<mots>.md`.
- Le tableau est `.depot-distant/tableau-tickets.md`, tenu par `uv run python outils/tableau.py`.
- Sur Jira : la page du ticket, ou l'outil en ligne de commande de l'équipe s'il existe.
