"""Liste des applications affichées sur la page d'accueil du portail."""

APPLICATIONS = [
    {
        "nom": "Délais fournisseurs",
        "description": "Délais moyens et maximums de livraison par fournisseur.",
        "lien": "/delais-fournisseurs",
        "statut": "en service",
    },
    {
        "nom": "Suivi des commandes du jour",
        "description": "Nombre de commandes, articles et CA net HT par canal pour une journée.",
        "lien": "/commandes-du-jour",
        "statut": "en service",
    },
    {
        "nom": "Prévision des commandes web",
        "description": "Prévision hebdomadaire des commandes web (projet en cours).",
        "lien": None,
        "statut": "à venir",
    },
    {
        "nom": "Ciblage des clients à risque",
        "description": "Liste des clients susceptibles de ne plus commander (projet en cours).",
        "lien": None,
        "statut": "à venir",
    },
]
