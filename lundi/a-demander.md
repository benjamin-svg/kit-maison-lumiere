# À demander avant de refaire le travail sur les vraies données

À envoyer avant lundi aux bonnes personnes. Sans ces réponses, Claude devinera, et vous aussi.

## Pour tous

- [ ] Un accès **en lecture seule** à BigQuery (rôles `BigQuery Data Viewer` sur les datasets utiles,
      `BigQuery Job User` sur le projet), et le Google Cloud CLI (`bq`) installé sur le poste.
- [ ] Le forfait BigQuery de l'entreprise (à la demande ou réservation) et un plafond par requête accepté
      (5 Go par défaut dans le kit).
- [ ] Le dépôt GitLab où ranger la couche sémantique et les analyses, et ses droits.
- [ ] Le droit d'utiliser `glab` avec un jeton personnel : qui le délivre, avec quels droits, pour combien de temps.

## Céline (analyses)

- [ ] Les **noms complets** des tables pour les questions habituelles : lignes de commande, commandes, clients,
      envois d'e-mails, calendrier des opérations. Et leur colonne de partition.
- [ ] Le **propriétaire** de chaque métrique (qui tranche « client actif », « CA net »), et les définitions déjà
      officielles.
- [ ] Une table (ou un fichier) qui relie chaque **campagne e-mail** à une opération commerciale. Sans elle, la
      question « l'e-mail a-t-il fait acheter ? » reste une hypothèse.
- [ ] Comment sont choisis les destinataires d'une campagne (tous les inscrits ? un tirage ?) : c'est ce qui dit
      si l'on a un groupe témoin.

## Olivier (prévision)

- [ ] Où vit le **calendrier commercial** (Orli, fichier du marketing, autre) et s'il garde ses **versions**
      (date d'annonce, déplacements).
- [ ] Ce que la logistique veut : commandes passées ou colis à préparer ? Avec ou sans annulations ?
- [ ] La **date d'annulation** des commandes (ou l'historique des statuts) : sans elle, une prévision passée est
      comparée à un réel qui change encore après coup.
- [ ] Où vit l'attribut **encombrant** dans le vrai catalogue (une colonne, une famille, une liste à part).
- [ ] Le choix pour la semaine 53 de 2026 (décalage de 364 jours, ou même numéro de semaine).
- [ ] Un **compte de service** pour le pipeline du lundi, le dataset où écrire `prevision_hebdo`, et qui reçoit
      l'alerte en cas d'échec.

## Augustin (churn)

- [ ] Le délai et la méthode d'**anonymisation** réels (après combien de temps, quels clients sont exclus, qui
      la lance), et le contact à l'équipe données.
- [ ] L'accord du **DPO** pour figer une photo par mois. Modèle de demande :

> Objet : conservation de photos mensuelles pour le modèle de churn
>
> Pour mesurer correctement le risque de perte des clients, nous souhaitons conserver chaque mois une photo
> des variables du modèle, calculées à cette date : récence, nombre et montant des commandes sur 12 mois,
> ouvertures et clics d'e-mails sur 90 jours, ancienneté, inscription aux e-mails. Les clients y sont désignés
> par un identifiant pseudonyme durable, sans nom, adresse ni e-mail. Durée de conservation proposée : <N> mois.
> Usage : apprentissage et contrôle du modèle de churn, par l'équipe e-commerce seulement. Sans ces photos,
> l'anonymisation des clients inactifs fait disparaître les clients perdus de l'historique, et le modèle
> sous-estime le risque. Pouvez-vous nous dire si ce traitement est possible, et à quelles conditions ?

- [ ] La table des e-mails garde-t-elle les **désinscrits** et leurs anciens envois, ou seulement les inscrits
      d'aujourd'hui ? (sinon, les variables e-mail des anciennes photos sont faussées)
- [ ] La requête qui a construit la table d'apprentissage du modèle actuel, et ses options (`bq show --model`).
- [ ] Ce que le CRM fera de la liste (taille de la campagne, groupe témoin accepté ou non).

## Maxime (portail et GitLab)

- [ ] L'offre GitLab de l'entreprise (Free, Premium, Ultimate) : les approbations obligatoires en dépendent.
- [ ] Les runners : partagés ou propres au groupe, image Docker publique acceptée, accès à PyPI ou miroir interne.
- [ ] La technique du vrai portail (langage, framework, commande de tests) : elle fixe `COMMANDE_TESTS`.
