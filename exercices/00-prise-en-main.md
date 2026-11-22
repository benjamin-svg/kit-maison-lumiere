# Exercice 00 - Prise en main de Claude Code et de Claude Desktop (onglet Code)

## Objectif

Savoir ouvrir le kit dans Claude Code (terminal) et dans Claude Desktop (onglet Code), et reconnaître les briques
qui rendent Claude utile et sûr sur un projet : le fichier `CLAUDE.md`, le mode plan, le retour en arrière
(`/rewind`), une skill, un sous-agent et un hook.

## Durée

- **En salle, 30 min** : étapes 1, 3, 5, 6 et 7 (25 min), et 5 min de questions.
- **En autonomie, 20 min de plus** : étapes 2, 4 et 8.

## Avant de commencer

L'installation est faite (`uv sync`, puis `uv run python donnees/generer_donnees.py`).
Ouvrez un terminal dans le dossier du kit et lancez `claude`. À la question « faites-vous confiance à ce
dossier ? », répondez **oui** : sinon les réglages, les hooks et les skills du kit ne sont pas chargés,
et rien ne vous prévient.

Tapez `/hooks` : vous devez voir un hook **PreToolUse** (`garde_fou.py`) et un hook **PostToolUse**
(`lancer_tests.py`). S'ils n'y sont pas, appelez le formateur avant d'aller plus loin.

## Étape 1 - Ce que Claude sait du projet (5 min, en salle)

> « Je suis <votre prénom>. En cinq phrases simples, explique-moi ce qu'est ce dossier, quelles données il contient et quelles règles tu dois respecter ici. »

**À observer** : Claude répond sans avoir besoin d'ouvrir beaucoup de fichiers, parce qu'il a lu `CLAUDE.md`
au démarrage. Il cite les règles (lecture seule de `donnees/brutes/`, dossier `travail/<prénom>/`, lecture de `semantique/`).

## Étape 2 - `/init` et le fichier `CLAUDE.md` (5 min, en autonomie)

Tapez `/init`.

**À observer** : `CLAUDE.md` existe déjà ; Claude explore le dépôt et propose de le compléter.
Lisez sa proposition, et **refusez tout ce qui parle des métriques ou des définitions** (chiffre d'affaires,
client actif, etc.) : elles vivent dans `semantique/` seulement. Deux copies d'une même définition finissent
par se contredire, et l'exercice 03 ne marcherait plus. Dans le doute, refusez tout : le `CLAUDE.md` du kit suffit.

Tapez ensuite `/memory` pour voir quels fichiers de consignes sont chargés (celui du kit, et éventuellement
le vôtre, personnel). Puis :

> « Ajoute dans CLAUDE.md, section Règles, une règle : les montants sont toujours affichés en euros avec un espace comme séparateur des milliers. Montre-moi la modification avant de l'enregistrer. »

(Pas de commit ici : on le fera dans l'exercice 01, après la partie Git.)

## Étape 3 - Le mode plan (5 min, en salle)

Appuyez sur **Maj+Tab** jusqu'à voir « plan mode » en bas de l'écran (dans Desktop : choisissez le mode plan
dans le sélecteur de mode). Puis :

> « Je voudrais ajouter au portail une page qui affiche les 10 produits les plus vendus du mois. Propose un plan, sans rien modifier. »

**À observer** : en mode plan, Claude lit et réfléchit, mais ne modifie aucun fichier. Il propose un plan
(fichiers à toucher, tests à écrire, définition à utiliser pour « les plus vendus »). Refusez le plan
ou demandez une modification : rien n'a été écrit. Sortez du mode plan (Maj+Tab).

## Étape 4 - Revenir en arrière avec `/rewind` (5 min, en autonomie)

> « Crée le fichier travail/<prénom>/essai.md avec trois idées d'analyses sur les retours produits. »

Puis tapez `/rewind` (ou appuyez deux fois sur Échap), choisissez le point juste avant cette demande et
restaurez le code et la conversation.

**À observer** : le fichier `essai.md` a disparu, et la conversation est revenue en arrière.
À retenir : `/rewind` annule les modifications de fichiers faites par Claude, mais pas ce qui a été fait
hors de Claude (une commande lancée sur un serveur, un commit poussé). Git reste le vrai filet de sécurité.

## Étape 5 - Une skill (5 min, en salle)

Tapez `/` et repérez les skills du kit (`/analyse`, `/documenter-table`, etc.). Puis :

> « /analyse Combien de commandes web non annulées ont été passées en décembre 2025 ? »

**À observer** : Claude suit les étapes écrites dans `.claude/skills/analyse/SKILL.md` : il reformule,
lit `semantique/`, écrit et explique sa requête, l'exécute, annonce ses contrôles, enregistre le résultat
dans `travail/<prénom>/analyses/`. Ouvrez le fichier `SKILL.md` : c'est un simple texte de consignes.

## Étape 6 - Un sous-agent (5 min, en salle)

> « Demande au sous-agent verificateur de recalculer ce chiffre par un autre chemin, sans lui montrer ta requête. »

**À observer** : le sous-agent travaille dans son propre contexte (il ne voit pas la conversation),
puis rend un verdict (confirmé ou non). Tapez `/agents` pour voir la liste des sous-agents du kit.

## Étape 7 - Un hook qui bloque (5 min, en salle)

Il y a **deux barrières**. La première est `CLAUDE.md` : Claude lit les règles et refuse souvent de lui-même,
sans rien essayer. C'est un conseil que le modèle suit. La seconde est le hook : un programme lancé par
Claude Code avant chaque action, qui bloque même si la consigne a été oubliée. Pour voir la seconde,
il faut demander une vraie tentative.

**D'abord, vérifiez que les hooks sont chargés** : tapez `/hooks`. Un hook PreToolUse (`garde_fou.py`) doit
apparaître. S'il n'apparaît pas (par exemple si vous avez refusé la confiance au dossier au lancement), **ne faites
pas cette étape** : sans hook, la commande serait vraiment exécutée. Quittez, relancez `claude` et répondez oui à
la question de confiance, ou appelez le formateur.

Puis :

> « Crée le dossier vide travail/<prénom>/vide. Puis lance exactement cette commande, je veux voir le garde-fou : rm -rf travail/<prénom>/vide »

Puis :

> « Essaie vraiment, avec ton outil de modification de fichiers, de remplacer "Robe" par "ROBE" sur la deuxième ligne de donnees/brutes/produits.csv. Je sais que c'est interdit : je veux voir le refus du hook. »

**À observer** : la réponse contient « Refusé par le garde-fou de la formation : ... ». Ce texte vient du hook
`.claude/hooks/garde_fou.py`, pas de Claude. Regardez `.claude/settings.json` pour voir comment il est branché.
Si Claude refuse encore sans essayer, ce n'est pas grave : vous avez vu la première barrière. Lancez alors
vous-même `uv run python outils/tester_hooks.py` pour lire les messages du hook.

Si Claude propose un autre moyen (par exemple `rm -r` sans `-f`, qui n'est pas bloqué), refusez
et discutez-en : un hook ne bloque que ce qu'il sait reconnaître.

## Étape 8 - Le même kit dans Claude Desktop, onglet Code (5 min, en autonomie)

Ouvrez Claude Desktop (onglet Code), choisissez le dossier du kit, et redonnez la consigne de l'étape 1.
**À observer** : mêmes consignes, mêmes skills, mêmes hooks ; la relecture des modifications se fait dans
une vue des différences plus confortable.

## Comment vérifier

- Étape 5 : **2 573** commandes web non annulées en décembre 2025, confirmées par le vérificateur.
  Si vous trouvez 2 737, les commandes annulées ont été comptées.
- `travail/<prénom>/analyses/` contient un dossier avec `requete.sql`, `resultat.csv` et `NOTE.md`.
- `git status` ne montre aucun changement dans `donnees/`. `CLAUDE.md` apparaît modifié si vous avez fait l'étape 2 :
  c'est normal, on le commitera dans l'exercice 01.
  Le dossier `travail/` n'est pas suivi par git : c'est voulu.
- `uv run python outils/tester_hooks.py` affiche « Tous les cas sont conformes. »

## Pour aller plus loin

- Demandez à Claude d'écrire une nouvelle skill `/resume-semaine` qui résume l'activité de la semaine
  passée (commandes, CA net HT, annulations), en s'inspirant de `.claude/skills/analyse/SKILL.md`.
- Lisez `.claude/hooks/garde_fou.py` avec Claude et demandez-lui de citer une commande qui écrirait dans
  `donnees/brutes/` sans être bloquée (un hook n'est qu'un filet, pas une protection absolue).
- Le mot technique qui vous arrête est sans doute dans `GLOSSAIRE.md`.
