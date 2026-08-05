def test_modal_aparece_na_primeira_visita(client, backend_falso):
    resposta = client.get("/home")
    assert b"modal-demo" in resposta.data


def test_marcar_como_visto_grava_na_sessao(client, backend_falso):
    client.get("/")
    assert client.post("/demo/modal-visto").status_code == 204
    with client.session_transaction() as sessao:
        assert sessao["demo_modal_visto"] is True


def test_modal_nao_reaparece_depois_de_visto(client, backend_falso):
    client.get("/")
    client.post("/demo/modal-visto")
    resposta = client.get("/home")
    assert b'id="modal-demo" class="modal fade show' not in resposta.data


def test_link_de_reabrir_esta_na_navbar(client, backend_falso):
    resposta = client.get("/home")
    assert b"Sobre esta demo" in resposta.data
