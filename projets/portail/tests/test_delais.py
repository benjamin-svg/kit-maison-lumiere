from app import delais


def test_page_delais_affiche_tous_les_fournisseurs(client):
    reponse = client.get("/delais-fournisseurs")
    assert reponse.status_code == 200
    assert "Atelier Douro" in reponse.text
    assert "Filature du Nord" in reponse.text
    assert "24 fournisseur(s)" in reponse.text


def test_filtre_pays(client):
    reponse = client.get("/api/delais-fournisseurs", params={"pays": "Portugal"})
    assert reponse.status_code == 200
    fournisseurs = reponse.json()
    assert len(fournisseurs) == 5
    assert {f["pays"] for f in fournisseurs} == {"Portugal"}


def test_filtre_pays_insensible_a_la_casse():
    assert len(delais.lire_delais("portugal")) == len(delais.lire_delais("Portugal"))


def test_liste_pays_sans_doublon():
    pays = delais.liste_pays()
    assert len(pays) == len(set(pays))
    assert "France" in pays


def test_delai_moyen_portugal():
    # valeur relevée sur la page le 15/12/2025
    assert delais.delai_moyen(delais.lire_delais("Portugal")) == 12


def test_page_affiche_le_delai_moyen(client):
    reponse = client.get("/delais-fournisseurs", params={"pays": "Portugal"})
    assert "Délai moyen des fournisseurs affichés" in reponse.text
