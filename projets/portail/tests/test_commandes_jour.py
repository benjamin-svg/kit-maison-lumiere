def test_commandes_du_jour_exclut_les_annulees(client, base_test, jour_test):
    reponse = client.get("/api/commandes-du-jour", params={"date": str(jour_test)})
    assert reponse.status_code == 200
    canaux = {c["canal"]: c for c in reponse.json()["canaux"]}
    assert canaux["WEB"]["nb_commandes"] == 1
    assert canaux["WEB"]["nb_articles"] == 3
    # 50 + 40 - 20 de retour ; la commande annulée (99) n'est pas comptée
    assert canaux["WEB"]["ca_net_ht"] == 70.0
    assert canaux["MAGASIN"]["ca_net_ht"] == 45.0


def test_date_par_defaut_est_la_derniere(client, base_test):
    reponse = client.get("/api/commandes-du-jour")
    assert reponse.json()["date"] == "2025-12-31"


def test_page_html_commandes(client, base_test, jour_test):
    reponse = client.get("/commandes-du-jour", params={"date": str(jour_test)})
    assert reponse.status_code == 200
    assert "MAGASIN" in reponse.text
    assert "annulées exclues" in reponse.text


def test_jour_sans_commande(client, base_test):
    reponse = client.get("/commandes-du-jour", params={"date": "2020-01-01"})
    assert reponse.status_code == 200
    assert "Aucune commande" in reponse.text
