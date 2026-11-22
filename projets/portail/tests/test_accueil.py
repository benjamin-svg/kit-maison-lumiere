from app.applications import APPLICATIONS


def test_accueil_liste_les_applications(client):
    reponse = client.get("/")
    assert reponse.status_code == 200
    for a in APPLICATIONS:
        assert a["nom"] in reponse.text


def test_api_applications(client):
    reponse = client.get("/api/applications")
    assert reponse.status_code == 200
    assert len(reponse.json()) == len(APPLICATIONS)
