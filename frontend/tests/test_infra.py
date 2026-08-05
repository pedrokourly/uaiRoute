def test_app_responde(client):
    resposta = client.get("/login")
    assert resposta.status_code == 200
