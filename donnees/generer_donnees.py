"""Génère les données fictives de Maison Lumière (e-commerce de mode).

Usage :
    uv run python donnees/generer_donnees.py

Produit :
    donnees/ecommerce.duckdb   base DuckDB avec toutes les tables
    donnees/brutes/*.csv       les mêmes tables au format CSV

Toutes les données sont inventées. La graine est fixe : deux exécutions
donnent exactement le même résultat.
"""

from __future__ import annotations

import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

GRAINE = 20251231
DOSSIER = Path(__file__).resolve().parent
DOSSIER_BRUTES = DOSSIER / "brutes"
CHEMIN_BASE = DOSSIER / "ecommerce.duckdb"

ORIGINE = pd.Timestamp("2016-01-01")  # début de l'historique simulé (non exporté)
DEBUT = pd.Timestamp("2023-01-01")  # début des données exportées
FIN = pd.Timestamp("2025-12-31")  # date d'extraction
DATE_REFERENCE = pd.Timestamp("2025-06-30")  # date de la photo churn
DELAI_ANONYMISATION = 730  # jours d'inactivité avant anonymisation
LANCEMENT_MARKETPLACE = pd.Timestamp("2024-03-01")

CANAUX = ["WEB", "MAGASIN", "MARKETPLACE"]
REGIONS = [
    "Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie",
    "Hauts-de-France", "Provence-Alpes-Côte d'Azur", "Grand Est", "Pays de la Loire",
    "Bretagne", "Normandie", "Bourgogne-Franche-Comté", "Centre-Val de Loire", "Corse",
]
POIDS_REGIONS = [0.26, 0.12, 0.09, 0.08, 0.07, 0.08, 0.07, 0.07, 0.06, 0.04, 0.03, 0.025, 0.005]


def jour(ts: pd.Timestamp) -> int:
    """Numéro de jour depuis ORIGINE."""
    return int((ts - ORIGINE).days)


# ---------------------------------------------------------------------------
# Calendrier commercial
# ---------------------------------------------------------------------------

def n_ieme_jour(annee: int, mois: int, jour_semaine: int, n: int) -> pd.Timestamp:
    """n-ième jour_semaine (0 = lundi) du mois ; n = -1 pour le dernier."""
    jours = pd.date_range(f"{annee}-{mois:02d}-01", periods=31, freq="D")
    jours = [j for j in jours if j.month == mois and j.weekday() == jour_semaine]
    return jours[n] if n < 0 else jours[n - 1]


def calendrier_commercial() -> pd.DataFrame:
    lignes = []

    def ajout(debut, fin, type_op, libelle, canaux):
        lignes.append(dict(date_debut=pd.Timestamp(debut), date_fin=pd.Timestamp(fin),
                           type_operation=type_op, libelle=libelle, canaux=canaux))

    ventes_privees = {
        2023: [("2023-03-15", "2023-03-19"), ("2023-10-04", "2023-10-08")],
        2024: [("2024-03-20", "2024-03-24"), ("2024-09-25", "2024-09-29")],
        2025: [("2025-04-02", "2025-04-06"), ("2025-10-08", "2025-10-12")],
    }
    livraison_offerte = {
        2023: [("2023-05-03", "2023-05-05"), ("2023-11-08", "2023-11-10")],
        2024: [("2024-04-17", "2024-04-19"), ("2024-11-06", "2024-11-08")],
        2025: [("2025-05-14", "2025-05-16"), ("2025-11-05", "2025-11-07")],
    }
    fete_des_meres = {2023: "2023-05-28", 2024: "2024-05-26", 2025: "2025-05-25"}
    for annee in (2023, 2024, 2025):
        d = n_ieme_jour(annee, 1, 2, 2)
        ajout(d, d + pd.Timedelta(days=27), "SOLDES", f"Soldes d'hiver {annee}", "TOUS")
        d = n_ieme_jour(annee, 6, 2, -1)
        ajout(d, d + pd.Timedelta(days=27), "SOLDES", f"Soldes d'été {annee}", "TOUS")
        d = n_ieme_jour(annee, 11, 4, 4)
        ajout(d, d + pd.Timedelta(days=3), "BLACK_FRIDAY", f"Black Friday {annee}", "TOUS")
        for i, (a, b) in enumerate(ventes_privees[annee], 1):
            ajout(a, b, "VENTE_PRIVEE", f"Vente privée {i} {annee}", "WEB")
        for i, (a, b) in enumerate(livraison_offerte[annee], 1):
            ajout(a, b, "LIVRAISON_OFFERTE", f"Livraison offerte {i} {annee}", "WEB")
        f = pd.Timestamp(fete_des_meres[annee])
        ajout(f - pd.Timedelta(days=10), f - pd.Timedelta(days=1), "FETE_DES_MERES",
              f"Fête des mères {annee}", "TOUS")
        ajout(f"{annee}-08-16", f"{annee}-09-07", "RENTREE", f"Rentrée {annee}", "TOUS")
        ajout(f"{annee}-12-01", f"{annee}-12-22", "NOEL", f"Noël {annee}", "TOUS")
    cal = pd.DataFrame(lignes).sort_values("date_debut").reset_index(drop=True)
    cal.insert(0, "id_operation", np.arange(1, len(cal) + 1))
    return cal


# Les changements de date connus entre deux versions du plan (id_operation ou libellé 2026 -> versions).
# Chaque version : (date de publication, date de début prévue, date de fin prévue).
CHANGEMENTS_PLAN = {
    "Vente privée 2 2024": [("2023-11-15", "2024-10-02", "2024-10-06"), ("2024-08-26", "2024-09-25", "2024-09-29")],
    "Vente privée 2 2025": [("2024-11-15", "2025-10-01", "2025-10-05"), ("2025-09-01", "2025-10-08", "2025-10-12")],
    "Livraison offerte 2 2025": [("2024-11-15", "2025-11-12", "2025-11-14"), ("2025-10-06", "2025-11-05", "2025-11-07")],
    "Vente privée 1 2026": [("2025-11-17", "2026-03-25", "2026-03-29"), ("2025-12-15", "2026-04-08", "2026-04-12")],
}


def plan_commercial(cal: pd.DataFrame) -> pd.DataFrame:
    """Le plan commercial tel qu'il était connu à chaque date de publication (une ligne par version).

    calendrier_commercial donne les dates réalisées. plan_commercial garde l'historique des versions :
    une opération annoncée puis déplacée a deux lignes. Le plan de l'année N est publié mi-novembre de
    l'année N-1 (le 15/11, et le 17/11/2025 pour 2026) ; quelques opérations sont déplacées en cours d'année.
    Ce tableau ne dépend d'aucun tirage aléatoire : il ne change aucune autre table.
    """
    lignes = []

    def ajouter(id_op, libelle, type_op, canaux, versions):
        for num, (dv, d, f) in enumerate(versions, 1):
            lignes.append(dict(id_operation=id_op, libelle=libelle, type_operation=type_op, canaux=canaux,
                               version=num, date_version=pd.Timestamp(dv),
                               date_debut=pd.Timestamp(d), date_fin=pd.Timestamp(f)))

    for op in cal.itertuples():
        versions = CHANGEMENTS_PLAN.get(op.libelle)
        if versions is None:
            versions = [(f"{op.date_debut.year - 1}-11-15", op.date_debut.date(), op.date_fin.date())]
        ajouter(op.id_operation, op.libelle, op.type_operation, op.canaux, versions)

    # plan 2026, publié le 17/11/2025 (mêmes règles que les années précédentes)
    pub = "2025-11-17"
    plan_2026 = []
    d = n_ieme_jour(2026, 1, 2, 2)
    plan_2026.append(("SOLDES", "Soldes d'hiver 2026", "TOUS", d, d + pd.Timedelta(days=27)))
    plan_2026.append(("VENTE_PRIVEE", "Vente privée 1 2026", "WEB", None, None))
    plan_2026.append(("LIVRAISON_OFFERTE", "Livraison offerte 1 2026", "WEB", pd.Timestamp("2026-05-13"), pd.Timestamp("2026-05-15")))
    f = pd.Timestamp("2026-05-31")
    plan_2026.append(("FETE_DES_MERES", "Fête des mères 2026", "TOUS", f - pd.Timedelta(days=10), f - pd.Timedelta(days=1)))
    d = n_ieme_jour(2026, 6, 2, -1)
    plan_2026.append(("SOLDES", "Soldes d'été 2026", "TOUS", d, d + pd.Timedelta(days=27)))
    plan_2026.append(("RENTREE", "Rentrée 2026", "TOUS", pd.Timestamp("2026-08-16"), pd.Timestamp("2026-09-07")))
    plan_2026.append(("VENTE_PRIVEE", "Vente privée 2 2026", "WEB", pd.Timestamp("2026-10-07"), pd.Timestamp("2026-10-11")))
    plan_2026.append(("LIVRAISON_OFFERTE", "Livraison offerte 2 2026", "WEB", pd.Timestamp("2026-11-04"), pd.Timestamp("2026-11-06")))
    d = n_ieme_jour(2026, 11, 4, 4)
    plan_2026.append(("BLACK_FRIDAY", "Black Friday 2026", "TOUS", d, d + pd.Timedelta(days=3)))
    plan_2026.append(("NOEL", "Noël 2026", "TOUS", pd.Timestamp("2026-12-01"), pd.Timestamp("2026-12-22")))
    id_op = int(cal.id_operation.max())
    for type_op, libelle, canaux, d, f in plan_2026:
        id_op += 1
        versions = CHANGEMENTS_PLAN.get(libelle) or [(pub, d.date(), f.date())]
        ajouter(id_op, libelle, type_op, canaux, versions)

    plan = pd.DataFrame(lignes).sort_values(["date_debut", "id_operation", "version"]).reset_index(drop=True)
    return plan[["id_operation", "version", "date_version", "libelle", "type_operation", "canaux",
                 "date_debut", "date_fin"]]


EFFETS = {
    #                   WEB   MAGASIN  MARKETPLACE
    "SOLDES": (1.55, 1.45, 1.30),
    "BLACK_FRIDAY": (2.60, 1.45, 1.80),
    "VENTE_PRIVEE": (1.85, 1.00, 1.00),
    "LIVRAISON_OFFERTE": (1.30, 1.00, 1.00),
    "FETE_DES_MERES": (1.15, 1.20, 1.05),
    "RENTREE": (1.10, 1.08, 1.05),
    "NOEL": (1.30, 1.40, 1.20),
}


def poids_journaliers(rng: np.random.Generator, cal: pd.DataFrame) -> tuple[pd.DatetimeIndex, np.ndarray]:
    """Intensité relative d'achat par jour et par canal (3 x nb_jours)."""
    dates = pd.date_range(ORIGINE, FIN, freq="D")
    n = len(dates)
    doy = dates.day_of_year.values
    dow = dates.day_of_week.values
    t = (dates - DEBUT).days.values / 365.25

    annuel = 1 + 0.16 * np.cos(2 * np.pi * (doy - 345) / 365.25) - 0.22 * np.exp(-((doy - 222) / 14) ** 2)
    semaine = np.array([
        [1.18, 1.02, 0.96, 0.95, 0.90, 0.82, 1.17],  # WEB
        [0.62, 0.85, 1.00, 0.95, 1.12, 1.82, 0.16],  # MAGASIN
        [1.05, 1.00, 1.00, 1.00, 0.98, 0.95, 1.02],  # MARKETPLACE
    ])
    tendance = np.vstack([
        1 + 0.09 * t,
        np.clip(1 - 0.035 * t, 0.7, None),
        np.ones(n),
    ])
    w = annuel[None, :] * semaine[:, dow] * tendance

    # Marketplace : lancement en mars 2024, montée en charge sur 6 mois
    age_mkp = (dates - LANCEMENT_MARKETPLACE).days.values
    w[2] *= np.clip(age_mkp / 180, 0, 1)

    # Jours fériés : magasins fermés
    feries = (dates.month == 1) & (dates.day == 1) | (dates.month == 5) & (dates.day == 1) | (
        dates.month == 12) & (dates.day == 25)
    w[1, feries] = 0.0

    # Opérations commerciales (uniquement sur la fenêtre exportée)
    for op in cal.itertuples():
        masque = (dates >= op.date_debut) & (dates <= op.date_fin)
        effet = np.array(EFFETS[op.type_operation])
        if op.type_operation == "SOLDES":
            # premier week-end de soldes plus fort, puis essoufflement
            rang = (dates[masque] - op.date_debut).days.values
            profil = 1 + (effet[:, None] - 1) * np.where(rang < 7, 1.6, np.where(rang < 14, 0.9, 0.45))
            w[:, masque] *= profil
        elif op.type_operation == "BLACK_FRIDAY":
            rang = (dates[masque] - op.date_debut).days.values
            profil = 1 + (effet[:, None] - 1) * np.array([1.4, 0.8, 0.7, 1.1])[rang]
            w[:, masque] *= profil
        else:
            w[:, masque] *= effet[:, None]
    # Semaine qui précède le Black Friday : attentisme
    for op in cal[cal.type_operation == "BLACK_FRIDAY"].itertuples():
        masque = (dates >= op.date_debut - pd.Timedelta(days=7)) & (dates < op.date_debut)
        w[0, masque] *= 0.85

    # Bruit journalier
    w *= rng.lognormal(0, 0.08, size=w.shape)
    # Normalisation : intensité moyenne 1 sur 2023 pour le web
    ref = (dates >= DEBUT) & (dates < pd.Timestamp("2024-01-01"))
    w /= w[0, ref].mean()
    return dates, w


# ---------------------------------------------------------------------------
# Produits
# ---------------------------------------------------------------------------

FAMILLES = {
    # famille: [(sous_famille, nb, prix_min, prix_max, encombrant)]
    "robe": [("robe", 50, 55, 120, False)],
    "chemise": [("chemise", 50, 38, 80, False)],
    "pull": [("pull", 45, 45, 110, False)],
    "pantalon": [("pantalon", 45, 42, 90, False)],
    "veste": [("veste", 30, 85, 180, False)],
    "enfant": [("vetement enfant", 60, 18, 48, False), ("bebe", 22, 14, 40, False),
               ("mobilier enfant", 8, 190, 590, True)],
    "maison": [("linge de maison", 34, 25, 140, False), ("decoration", 14, 14, 60, False),
               ("mobilier", 8, 240, 890, True), ("tapis", 4, 120, 380, True)],
    "accessoire": [("accessoire", 30, 14, 60, False)],
}

MOTS = {
    "robe": (["Robe portefeuille", "Robe chemise", "Robe longue", "Robe trapèze", "Robe plissée"],
             ["en lin", "en coton", "fleurie", "à rayures", "unie", "en viscose"]),
    "chemise": (["Chemise", "Chemisier", "Blouse", "Chemise oxford"],
                ["en popeline", "en lin", "à col claudine", "rayée", "brodée"]),
    "pull": (["Pull", "Gilet", "Cardigan", "Pull marin"], ["en laine", "en cachemire", "torsadé", "col rond", "col V"]),
    "pantalon": (["Pantalon", "Chino", "Jean", "Pantalon large"], ["en coton", "en velours", "droit", "fuselé"]),
    "veste": (["Veste", "Blazer", "Caban", "Trench"], ["en laine", "en coton", "matelassée", "déperlante"]),
    "vetement enfant": (["Robe enfant", "Chemise enfant", "Pull enfant", "Bermuda enfant", "Short enfant"],
                        ["en coton", "à smocks", "rayé", "en velours"]),
    "bebe": (["Barboteuse", "Body", "Grenouillère", "Brassière"], ["en coton bio", "en jersey", "brodé"]),
    "mobilier enfant": (["Lit enfant", "Commode enfant", "Armoire enfant", "Lit à barreaux"], ["en hêtre", "laqué blanc"]),
    "linge de maison": (["Housse de couette", "Taie d'oreiller", "Nappe", "Plaid", "Drap"],
                        ["en lin lavé", "en percale", "en gaze de coton", "à carreaux"]),
    "decoration": (["Coussin", "Bougie", "Vase", "Cadre"], ["en céramique", "en lin", "parfumée"]),
    "mobilier": (["Fauteuil", "Banc", "Console", "Bibliothèque"], ["en chêne", "en rotin", "en métal"]),
    "tapis": (["Tapis", "Tapis berbère", "Tapis tressé"], ["en jute", "en laine", "en coton"]),
    "accessoire": (["Foulard", "Ceinture", "Sac", "Bonnet", "Chapeau"], ["en soie", "en cuir", "en paille", "en laine"]),
}


def generer_produits(rng: np.random.Generator) -> pd.DataFrame:
    lignes = []
    for famille, sous in FAMILLES.items():
        for sous_famille, nb, pmin, pmax, encombrant in sous:
            noms, qualites = MOTS[sous_famille]
            for _ in range(nb):
                gamme = rng.choice(["ESSENTIEL", "SIGNATURE", "PRESTIGE"], p=[0.55, 0.35, 0.10])
                mult = {"ESSENTIEL": 0.85, "SIGNATURE": 1.05, "PRESTIGE": 1.35}[gamme]
                prix = rng.uniform(pmin, pmax) * mult
                prix = np.floor(prix) + 0.83 if prix > 20 else round(prix, 2)  # prix TTC « psychologiques »
                lignes.append(dict(
                    libelle=f"{rng.choice(noms)} {rng.choice(qualites)}",
                    famille=famille, sous_famille=sous_famille, gamme=gamme,
                    prix_ht=round(float(prix), 2), encombrant=bool(encombrant)))
    produits = pd.DataFrame(lignes)
    produits.insert(0, "id_produit", np.arange(1001, 1001 + len(produits)))
    return produits


# ---------------------------------------------------------------------------
# Personnes, identités clients, commandes
# ---------------------------------------------------------------------------

def generer_personnes(rng: np.random.Generator, dates: pd.DatetimeIndex, w: np.ndarray) -> pd.DataFrame:
    n_anciens, n_nouveaux = 17500, 7300
    j_debut, j_fin = jour(DEBUT), jour(FIN)
    # Anciens clients : créés entre 2016 et 2022, un peu plus nombreux récemment
    pa = np.linspace(0.8, 1.2, j_debut)
    pa /= pa.sum()
    crea_anciens = rng.choice(j_debut, size=n_anciens, p=pa)
    # Nouveaux clients : recrutés au rythme de l'activité (soldes, Black Friday...)
    pn = (w[0, j_debut:] * 1.2 + w[1, j_debut:] * 0.6 + w[2, j_debut:] * 0.4)
    pn = pn / pn.sum()
    crea_nouveaux = j_debut + rng.choice(j_fin - j_debut + 1, size=n_nouveaux, p=pn)
    creation = np.concatenate([crea_anciens, crea_nouveaux])
    n = len(creation)

    profil = rng.choice(3, size=n, p=[0.55, 0.33, 0.12])  # 0 web, 1 magasin, 2 omnicanal
    parts = np.array([[0.82, 0.12, 0.06], [0.22, 0.78, 0.00], [0.48, 0.40, 0.12]])[profil]
    parts = parts * rng.dirichlet([8, 8, 8], size=n) * 3
    parts /= parts.sum(axis=1, keepdims=True)

    canal_acq = np.empty(n, dtype=object)
    choix_web = rng.choice(["RECHERCHE", "RESEAUX_SOCIAUX", "NEWSLETTER", "PARRAINAGE", "ACCES_DIRECT"],
                           size=n, p=[0.35, 0.25, 0.10, 0.10, 0.20])
    premier_canal = np.array([rng.choice(3, p=p) for p in parts])
    premier_canal[(premier_canal == 2) & (creation < jour(LANCEMENT_MARKETPLACE))] = 0
    canal_acq[:] = choix_web
    canal_acq[premier_canal == 1] = "MAGASIN"
    canal_acq[premier_canal == 2] = "MARKETPLACE"
    mult_acq = pd.Series(canal_acq).map({"RECHERCHE": 1.0, "RESEAUX_SOCIAUX": 0.8, "NEWSLETTER": 1.1,
                                         "PARRAINAGE": 1.25, "ACCES_DIRECT": 1.05, "MAGASIN": 1.0,
                                         "MARKETPLACE": 0.7}).values

    rythme = rng.gamma(1.5, 2.7, size=n) * mult_acq  # commandes par an à intensité 1
    vie1 = rng.exponential(1.0, size=n) * 900 * (rythme / 4.0) ** 0.45 * rng.lognormal(0, 0.45, size=n)
    fin1 = creation + vie1.astype(int)
    reveil = rng.random(n) < 0.24
    debut2 = fin1 + rng.integers(300, 1300, size=n)
    fin2 = debut2 + (rng.exponential(1.0, size=n) * 420).astype(int)
    debut2 = np.where(reveil, debut2, -1)
    fin2 = np.where(reveil, fin2, -1)

    engagement = np.clip(rng.beta(2.2, 5.5, size=n) * (0.75 + 0.25 * np.minimum(rythme, 8) / 3), 0.01, 0.95)
    optin = rng.random(n) < 0.62
    region = rng.choice(REGIONS, size=n, p=np.array(POIDS_REGIONS) / sum(POIDS_REGIONS))
    sans_commande = rng.random(n) < 0.07  # compte créé sans achat immédiat
    carte_fidelite = rng.random(n) < np.where(profil == 1, 0.55, 0.25)  # pas de purge pour ces clients

    return pd.DataFrame(dict(
        personne=np.arange(n), creation=creation, rythme=rythme, fin1=fin1, debut2=debut2, fin2=fin2,
        p_web=parts[:, 0], p_mag=parts[:, 1], p_mkp=parts[:, 2], premier_canal=premier_canal,
        canal_acquisition=canal_acq, engagement=engagement, optin=optin, region=region,
        sans_commande=sans_commande, carte_fidelite=carte_fidelite))


def generer_achats(rng: np.random.Generator, pers: pd.DataFrame, w: np.ndarray) -> pd.DataFrame:
    """Dates et canaux des commandes de chaque personne (toutes périodes confondues)."""
    j_fin = jour(FIN)
    cum = np.concatenate([np.zeros((3, 1)), np.cumsum(w, axis=1)], axis=1)
    morceaux = []
    periodes = [(pers.creation.values, np.minimum(pers.fin1.values, j_fin))]
    m2 = pers.debut2.values >= 0
    periodes.append((np.where(m2, pers.debut2.values, 0), np.where(m2, np.minimum(pers.fin2.values, j_fin), -1)))
    parts = pers[["p_web", "p_mag", "p_mkp"]].values
    for debut, fin in periodes:
        valide = (fin >= debut) & (debut <= j_fin)
        for c in range(3):
            d = np.where(valide, debut, 0)
            f = np.where(valide, fin, 0)
            masse = np.where(valide, cum[c, f + 1] - cum[c, d], 0.0)
            attendu = pers.rythme.values * parts[:, c] * masse / 365.25
            nb = rng.poisson(attendu)
            idx = np.repeat(np.arange(len(pers)), nb)
            u = cum[c, d[idx]] + rng.random(len(idx)) * (cum[c, f[idx] + 1] - cum[c, d[idx]])
            j = np.searchsorted(cum[c], u, side="right") - 1
            morceaux.append(pd.DataFrame(dict(personne=idx, jour=j, canal=c)))
    # Commande d'acquisition le jour de la création du compte
    acq = pers[~pers.sans_commande]
    morceaux.append(pd.DataFrame(dict(personne=acq.personne.values, jour=acq.creation.values,
                                      canal=acq.premier_canal.values)))
    achats = pd.concat(morceaux, ignore_index=True)
    achats = achats[achats.jour <= j_fin]
    return achats.sort_values(["personne", "jour"]).reset_index(drop=True)


def construire_identites(pers: pd.DataFrame, achats: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Applique la règle d'anonymisation : après 730 jours sans achat, l'identité est effacée
    (sauf pour les porteurs de carte de fidélité). Une personne qui revient ensuite reçoit
    un nouvel identifiant client."""
    j_debut, j_fin = jour(DEBUT), jour(FIN)
    ev = pd.concat([
        pd.DataFrame(dict(personne=pers.personne.values, jour=pers.creation.values, achat=-1)),
        achats.assign(achat=achats.index.values)[["personne", "jour", "achat"]],
    ], ignore_index=True).sort_values(["personne", "jour", "achat"]).reset_index(drop=True)
    ecart = ev.groupby("personne").jour.diff()
    sans_carte = ev.personne.map(pers.set_index("personne").carte_fidelite).eq(False).values
    rupture = ((ecart > DELAI_ANONYMISATION) & sans_carte).astype(int)
    ev["rang_identite"] = rupture.groupby(ev.personne).cumsum()
    ident = ev.groupby(["personne", "rang_identite"]).agg(debut=("jour", "min"), dernier=("jour", "max")).reset_index()
    ident["date_anonymisation"] = ident.dernier + DELAI_ANONYMISATION
    carte = ident.personne.map(pers.set_index("personne").carte_fidelite).values
    ident["anonymise"] = (ident.date_anonymisation <= j_fin) & ~carte
    ident = ident[~ident.anonymise | (ident.date_anonymisation >= j_debut)].copy()
    ident = ident.sort_values(["debut", "personne"]).reset_index(drop=True)
    ident["id_client"] = np.arange(100001, 100001 + len(ident))
    achats = achats.copy()
    achats["rang_identite"] = ev[ev.achat >= 0].set_index("achat").rang_identite.reindex(achats.index).values
    achats = achats.merge(ident[["personne", "rang_identite", "id_client", "anonymise"]],
                          on=["personne", "rang_identite"], how="left")
    return ident, achats


def generer_lignes(rng, commandes: pd.DataFrame, produits: pd.DataFrame, cal: pd.DataFrame) -> pd.DataFrame:
    n_cmd = len(commandes)
    canal = commandes.canal.values
    nb_lignes = 1 + rng.poisson(np.where(canal == "WEB", 1.35, np.where(canal == "MAGASIN", 1.0, 0.5)))
    idx = np.repeat(np.arange(n_cmd), nb_lignes)
    dates = commandes.date_commande.values[idx]
    mois = pd.DatetimeIndex(dates).month.values
    canal_l = canal[idx]

    familles = produits.sous_famille.unique().tolist()
    base = {"robe": 1.2, "chemise": 1.1, "pull": 1.0, "pantalon": 1.0, "veste": 0.45, "vetement enfant": 1.3,
            "bebe": 0.6, "mobilier enfant": 0.10, "linge de maison": 0.6, "decoration": 0.35, "mobilier": 0.09,
            "tapis": 0.06, "accessoire": 0.5}
    saison = np.ones((13, len(familles)))
    for k, f in enumerate(familles):
        for m in range(1, 13):
            s = 1.0
            if f == "robe":
                s = 1.6 if m in (4, 5, 6, 7) else 0.7 if m in (11, 12, 1) else 1.0
            elif f in ("pull", "veste"):
                s = 1.7 if m in (10, 11, 12, 1) else 0.5 if m in (5, 6, 7, 8) else 1.0
            elif f in ("vetement enfant", "mobilier enfant"):
                s = 1.5 if m in (8, 9) else 1.0
            elif f in ("linge de maison", "decoration", "mobilier", "tapis"):
                s = 1.5 if m in (11, 12) else 1.0
            saison[m, k] = s * base[f]
    # le mobilier et les tapis se vendent surtout en ligne
    proba_mois = saison / saison.sum(axis=1, keepdims=True)
    choix_sf = np.empty(len(idx), dtype=int)
    u = rng.random(len(idx))
    for m in range(1, 13):
        sel = mois == m
        choix_sf[sel] = np.searchsorted(np.cumsum(proba_mois[m]), u[sel], side="right")
    choix_sf = np.minimum(choix_sf, len(familles) - 1)
    lourd = np.isin(np.array(familles)[choix_sf], ["mobilier", "mobilier enfant", "tapis"])
    remplace = lourd & (canal_l != "WEB") & (rng.random(len(idx)) < 0.8)
    choix_sf[remplace] = familles.index("decoration")

    # produit dans la sous-famille (quelques best-sellers)
    id_produit = np.empty(len(idx), dtype=int)
    prix_ht = np.empty(len(idx))
    for k, f in enumerate(familles):
        sel = np.where(choix_sf == k)[0]
        cand = produits[produits.sous_famille == f]
        poids = 1 / np.arange(1, len(cand) + 1) ** 0.6
        poids = rng.permutation(poids)
        pick = rng.choice(len(cand), size=len(sel), p=poids / poids.sum())
        id_produit[sel] = cand.id_produit.values[pick]
        prix_ht[sel] = cand.prix_ht.values[pick]

    quantite = 1 + (rng.random(len(idx)) < np.where(np.isin(np.array(familles)[choix_sf], ["bebe", "linge de maison", "decoration"]), 0.25, 0.07)).astype(int)

    # remises selon les opérations
    taux = np.zeros(len(idx))
    dates_ts = pd.DatetimeIndex(dates)
    for op in cal.itertuples():
        sel = (dates_ts >= op.date_debut) & (dates_ts <= op.date_fin)
        if op.canaux == "WEB":
            sel &= canal_l == "WEB"
        r = rng.random(sel.sum())
        if op.type_operation == "SOLDES":
            taux[sel] = np.where(r < 0.65, rng.choice([0.3, 0.4, 0.5], size=sel.sum(), p=[0.5, 0.35, 0.15]), 0)
        elif op.type_operation == "BLACK_FRIDAY":
            taux[sel] = np.where(r < 0.8, 0.2, 0)
        elif op.type_operation == "VENTE_PRIVEE":
            taux[sel] = np.where(r < 0.7, 0.25, 0)
    promo = (taux == 0) & (rng.random(len(idx)) < 0.04)
    taux[promo] = 0.1
    brut = quantite * prix_ht
    remise = np.round(brut * taux, 2)
    montant = np.round(brut - remise, 2)

    # retours
    sf = np.array(familles)[choix_sf]
    p_ret = pd.Series(sf).map({"robe": 0.24, "chemise": 0.16, "pull": 0.13, "pantalon": 0.21, "veste": 0.15,
                               "vetement enfant": 0.10, "bebe": 0.07, "mobilier enfant": 0.06,
                               "linge de maison": 0.06, "decoration": 0.04, "mobilier": 0.08, "tapis": 0.07,
                               "accessoire": 0.05}).values
    p_ret = p_ret * np.where(canal_l == "WEB", 1.0, np.where(canal_l == "MAGASIN", 0.2, 0.8))
    p_ret = p_ret * np.where(taux >= 0.3, 0.7, 1.0)
    statut_l = commandes.statut.values[idx]
    retour = (rng.random(len(idx)) < p_ret) & (statut_l == "LIVREE")
    q_ret = np.where(retour, np.where(quantite == 2, rng.integers(1, 3, len(idx)), 1), 0)
    m_ret = np.round(montant * q_ret / quantite, 2)

    return pd.DataFrame(dict(
        id_ligne=np.arange(1, len(idx) + 1), id_commande=commandes.id_commande.values[idx],
        id_produit=id_produit, quantite=quantite, prix_unitaire_ht=np.round(prix_ht, 2),
        remise_ht=remise, montant_ht=montant, quantite_retournee=q_ret, montant_retourne_ht=m_ret))


def generer_emails(rng, clients: pd.DataFrame, ident: pd.DataFrame, pers: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par envoi : campagne hebdomadaire envoyée à une partie des clients inscrits."""
    actifs = clients[~clients.anonymise & clients.optin_email].copy()
    actifs = actifs.merge(ident[["id_client", "personne"]], on="id_client").merge(
        pers[["personne", "creation", "fin1", "debut2", "fin2", "engagement"]], on="personne")
    crea = jour_vec(actifs.date_creation)
    lignes = []
    campagnes = pd.date_range("2023-01-03", FIN, freq="7D")
    types = ["NEWSLETTER", "NOUVEAUTES", "PROMOTION", "NEWSLETTER"]
    id_envoi = 0
    for k, d in enumerate(campagnes):
        jd = jour(d)
        cible = (crea <= jd) & (rng.random(len(actifs)) < 0.45)
        sel = actifs[cible]
        vivant = ((jd >= sel.creation) & (jd <= sel.fin1)) | ((sel.debut2 >= 0) & (jd >= sel.debut2) & (jd <= sel.fin2))
        p = np.where(vivant, sel.engagement, sel.engagement * 0.12)
        ouvert = rng.random(len(sel)) < p
        clique = ouvert & (rng.random(len(sel)) < np.where(vivant, 0.24, 0.10))
        n = len(sel)
        lignes.append(pd.DataFrame(dict(
            id_envoi=np.arange(id_envoi + 1, id_envoi + n + 1), id_campagne=k + 1, type_campagne=types[k % 4],
            id_client=sel.id_client.values, date_envoi=d, ouvert=ouvert, clique=clique)))
        id_envoi += n
    return pd.concat(lignes, ignore_index=True)


def jour_vec(s: pd.Series) -> np.ndarray:
    return (pd.to_datetime(s) - ORIGINE).dt.days.values


SQL_SNAPSHOT = """
CREATE OR REPLACE TABLE clients_churn_snapshot AS
WITH ref AS (SELECT DATE '{ref}' AS d),
cmd AS (
    SELECT c.id_client, c.id_commande, c.date_commande, c.canal,
           SUM(CAST(l.montant_ht AS DECIMAL(18, 2)) - CAST(l.montant_retourne_ht AS DECIMAL(18, 2))) AS montant_net_ht,
           SUM(CAST(l.montant_retourne_ht AS DECIMAL(18, 2))) AS montant_retourne_ht
    FROM commandes c JOIN lignes_commande l USING (id_commande)
    WHERE c.statut <> 'ANNULEE' AND c.id_client IS NOT NULL
    GROUP BY ALL
),
avant AS (
    SELECT id_client,
           MAX(date_commande) AS derniere_avant,
           COUNT(*) AS nb_commandes_total,
           COUNT(*) FILTER (WHERE date_commande > (SELECT d FROM ref) - INTERVAL 365 DAY) AS nb_commandes_12m,
           COALESCE(SUM(montant_net_ht) FILTER (WHERE date_commande > (SELECT d FROM ref) - INTERVAL 365 DAY), 0) AS montant_12m_ht,
           SUM(montant_net_ht) AS montant_total_ht,
           SUM(montant_retourne_ht) AS montant_retourne_total_ht
    FROM cmd WHERE date_commande <= (SELECT d FROM ref)
    GROUP BY id_client
),
canaux AS (
    SELECT id_client, canal AS canal_principal
    FROM (SELECT id_client, canal, COUNT(*) AS n FROM cmd
          WHERE date_commande <= (SELECT d FROM ref) GROUP BY ALL)
    QUALIFY ROW_NUMBER() OVER (PARTITION BY id_client ORDER BY n DESC, canal) = 1
),
apres AS (
    SELECT id_client, COUNT(*) AS nb_apres
    FROM cmd WHERE date_commande > (SELECT d FROM ref)
      AND date_commande <= (SELECT d FROM ref) + INTERVAL 182 DAY
    GROUP BY id_client
),
toutes AS (
    SELECT id_client, MAX(date_commande) AS date_derniere_commande FROM cmd GROUP BY id_client
),
mails AS (
    SELECT id_client,
           COUNT(*) AS envois_email_90j,
           COUNT(*) FILTER (WHERE ouvert) AS ouvertures_email_90j,
           COUNT(*) FILTER (WHERE clique) AS clics_email_90j
    FROM emails
    WHERE date_envoi > (SELECT d FROM ref) - INTERVAL 90 DAY AND date_envoi <= (SELECT d FROM ref)
    GROUP BY id_client
)
SELECT cl.id_client,
       (SELECT d FROM ref) AS date_reference,
       cl.region, cl.canal_acquisition, cl.optin_email,
       DATE_DIFF('day', cl.date_creation, (SELECT d FROM ref)) AS anciennete_jours,
       DATE_DIFF('day', a.derniere_avant, (SELECT d FROM ref)) AS recence_jours,
       a.nb_commandes_12m, a.nb_commandes_total,
       CAST(ROUND(a.montant_12m_ht, 2) AS DOUBLE) AS montant_12m_ht,
       CAST(ROUND(a.montant_total_ht / a.nb_commandes_total, 2) AS DOUBLE) AS panier_moyen_ht,
       CAST(ROUND(CASE WHEN a.montant_total_ht + a.montant_retourne_total_ht > 0
                  THEN a.montant_retourne_total_ht / (a.montant_total_ht + a.montant_retourne_total_ht) ELSE 0 END, 3)
            AS DOUBLE) AS taux_retour,
       k.canal_principal,
       COALESCE(m.envois_email_90j, 0) AS envois_email_90j,
       COALESCE(m.ouvertures_email_90j, 0) AS ouvertures_email_90j,
       COALESCE(m.clics_email_90j, 0) AS clics_email_90j,
       t.date_derniere_commande,
       CASE WHEN COALESCE(p.nb_apres, 0) = 0 THEN 1 ELSE 0 END AS perdu_6m
FROM clients cl
JOIN avant a USING (id_client)
JOIN canaux k USING (id_client)
LEFT JOIN apres p USING (id_client)
LEFT JOIN toutes t USING (id_client)
LEFT JOIN mails m USING (id_client)
WHERE cl.date_creation <= (SELECT d FROM ref)
ORDER BY cl.id_client
"""


def construire(verbeux: bool = True) -> dict:
    """Construit toutes les tables en mémoire. Renvoie un dictionnaire de DataFrames
    (les clés qui commencent par « _ » sont internes et ne sont pas exportées)."""
    rng = np.random.default_rng(GRAINE)
    cal = calendrier_commercial()
    dates, w = poids_journaliers(rng, cal)
    produits = generer_produits(rng)
    pers = generer_personnes(rng, dates, w)
    achats = generer_achats(rng, pers, w)
    ident, achats = construire_identites(pers, achats)

    # --- clients
    ident = ident.merge(pers, on="personne")
    reapparu = ident.rang_identite > 0
    canal_acq = ident.canal_acquisition.where(~reapparu, pd.Series(
        rng.choice(["RECHERCHE", "RESEAUX_SOCIAUX", "ACCES_DIRECT", "NEWSLETTER"], size=len(ident)),
        index=ident.index))
    optin = ident.optin & ~ident.anonymise
    clients = pd.DataFrame(dict(
        id_client=ident.id_client.values,
        date_creation=ORIGINE + pd.to_timedelta(ident.debut.values, unit="D"),
        canal_acquisition=canal_acq.values,
        region=ident.region.values,
        email_hash=[f"h{rng.integers(16**11, 16**12):012x}" for _ in range(len(ident))],
        optin_email=optin.values,
        carte_fidelite=ident.carte_fidelite.values,
        anonymise=ident.anonymise.values,
        date_anonymisation=pd.Series(ORIGINE + pd.to_timedelta(ident.date_anonymisation.values, unit="D")).where(
            ident.anonymise.values).values,
    ))
    anon = clients.anonymise.values
    for col in ("canal_acquisition", "region", "email_hash"):
        clients[col] = clients[col].astype(object)
        clients.loc[anon, col] = None
    clients.loc[anon, "date_creation"] = pd.NaT

    # --- commandes (fenêtre exportée)
    achats = achats[achats.jour >= jour(DEBUT)].copy()
    achats = achats.sort_values(["jour", "personne"]).reset_index(drop=True)
    n = len(achats)
    date_cmd = ORIGINE + pd.to_timedelta(achats.jour.values, unit="D")
    canal = np.array(CANAUX)[achats.canal.values]
    bf = np.zeros(n, dtype=bool)
    for op in cal[cal.type_operation == "BLACK_FRIDAY"].itertuples():
        bf |= (date_cmd >= op.date_debut) & (date_cmd <= op.date_fin)
    p_annul = np.where(canal == "WEB", 0.05, np.where(canal == "MAGASIN", 0.006, 0.04)) * np.where(bf, 1.8, 1.0)
    statut = np.where(rng.random(n) < p_annul, "ANNULEE", "LIVREE").astype(object)
    recent = (date_cmd > FIN - pd.Timedelta(days=4)) & (canal != "MAGASIN") & (statut == "LIVREE")
    statut[recent] = "EN_COURS"
    id_client = achats.id_client.astype("Int64").where(~achats.anonymise.astype(bool))
    commandes = pd.DataFrame(dict(id_commande=np.arange(5000001, 5000001 + n), id_client=id_client.values,
                                  date_commande=date_cmd, canal=canal, statut=statut))
    lignes = generer_lignes(rng, commandes, produits, cal)

    tot = lignes.groupby("id_commande").agg(nb_articles=("quantite", "sum"), ht=("montant_ht", "sum"))
    commandes = commandes.merge(tot, on="id_commande", how="left")
    ttc = (commandes.ht * 1.2).round(2)
    port = np.where((commandes.canal == "WEB") & (ttc < 80), 4.90, 0.0)
    commandes["frais_port_ttc"] = port
    commandes["montant_ttc"] = (ttc + port).round(2)
    commandes = commandes.drop(columns="ht")

    clients_emails = clients.merge(ident[["id_client"]], on="id_client")
    emails = generer_emails(rng, clients_emails, ident, pers)

    # --- agrégat quotidien par canal
    enc = produits.set_index("id_produit").encombrant
    lj = lignes.merge(commandes[["id_commande", "date_commande", "canal", "statut"]], on="id_commande")
    lj["q_enc"] = lj.quantite * lj.id_produit.map(enc).astype(int)
    lj["net"] = lj.montant_ht - lj.montant_retourne_ht
    valide = lj.statut != "ANNULEE"
    agg = lj.groupby(["date_commande", "canal"]).agg(ca_ht=("net", "sum")).reset_index()
    agg2 = lj[valide].groupby(["date_commande", "canal"]).agg(
        nb_commandes=("id_commande", "nunique"), nb_articles=("quantite", "sum"),
        nb_articles_encombrants=("q_enc", "sum")).reset_index()
    commandes_jour = agg2.merge(agg, on=["date_commande", "canal"], how="outer").fillna(0)
    commandes_jour = commandes_jour.rename(columns={"date_commande": "date"})
    for c in ("nb_commandes", "nb_articles", "nb_articles_encombrants"):
        commandes_jour[c] = commandes_jour[c].astype(int)
    commandes_jour["ca_ht"] = commandes_jour.ca_ht.round(2)
    commandes_jour = commandes_jour[["date", "canal", "nb_commandes", "nb_articles",
                                     "nb_articles_encombrants", "ca_ht"]].sort_values(["date", "canal"])

    return dict(produits=produits, clients=clients, commandes=commandes, lignes_commande=lignes,
                emails=emails, calendrier_commercial=cal, commandes_jour=commandes_jour,
                plan_commercial=plan_commercial(cal), _personnes=pers, _identites=ident, _achats=achats)


def ecrire(tables: dict) -> duckdb.DuckDBPyConnection:
    DOSSIER_BRUTES.mkdir(parents=True, exist_ok=True)
    if CHEMIN_BASE.exists():
        CHEMIN_BASE.unlink()
    con = duckdb.connect(str(CHEMIN_BASE))
    ordre = ["produits", "clients", "commandes", "lignes_commande", "emails",
             "calendrier_commercial", "commandes_jour", "plan_commercial"]
    for nom in ordre:
        df = tables[nom]
        con.register("tmp_df", df)
        con.execute(f"CREATE TABLE {nom} AS SELECT * FROM tmp_df")
        con.unregister("tmp_df")
    # types de dates propres
    con.execute("ALTER TABLE commandes ALTER date_commande TYPE DATE")
    con.execute("ALTER TABLE clients ALTER date_creation TYPE DATE")
    con.execute("ALTER TABLE clients ALTER date_anonymisation TYPE DATE")
    con.execute("ALTER TABLE emails ALTER date_envoi TYPE DATE")
    con.execute("ALTER TABLE calendrier_commercial ALTER date_debut TYPE DATE")
    con.execute("ALTER TABLE calendrier_commercial ALTER date_fin TYPE DATE")
    con.execute("ALTER TABLE commandes_jour ALTER date TYPE DATE")
    for col in ("date_version", "date_debut", "date_fin"):
        con.execute(f"ALTER TABLE plan_commercial ALTER {col} TYPE DATE")
    con.execute(SQL_SNAPSHOT.format(ref=DATE_REFERENCE.date()))
    for nom in ordre + ["clients_churn_snapshot"]:
        con.execute(f"COPY {nom} TO '{(DOSSIER_BRUTES / (nom + '.csv')).as_posix()}' (HEADER, DELIMITER ',')")
    return con


def main() -> None:
    t0 = time.time()
    print("Génération des données fictives de Maison Lumière...")
    tables = construire()
    con = ecrire(tables)
    print(f"\nBase : {CHEMIN_BASE.relative_to(DOSSIER.parent)}")
    print(f"CSV  : {DOSSIER_BRUTES.relative_to(DOSSIER.parent)}/\n")
    print(f"{'table':<26}{'lignes':>12}")
    for nom in ["produits", "clients", "commandes", "lignes_commande", "emails",
                "calendrier_commercial", "plan_commercial", "commandes_jour", "clients_churn_snapshot"]:
        n = con.execute(f"SELECT COUNT(*) FROM {nom}").fetchone()[0]
        print(f"{nom:<26}{n:>12,}".replace(",", " "))
    d1, d2 = con.execute("SELECT MIN(date_commande), MAX(date_commande) FROM commandes").fetchone()
    print(f"\nPériode des commandes : du {d1} au {d2}")
    print(f"Date de référence de la photo churn : {DATE_REFERENCE.date()}")
    con.close()
    print(f"Terminé en {time.time() - t0:.1f} s.")


if __name__ == "__main__":
    main()
