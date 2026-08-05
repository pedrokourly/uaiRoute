from unittest.mock import patch


class RespostaFalsa:
    def __init__(self, dados, status_code=200):
        self._dados = dados
        self.status_code = status_code
        self.ok = status_code == 200

    def json(self):
        return self._dados


def test_direcoes_exige_sessao(client):
    resposta = client.post("/api/rota/direcoes", json={"coordinates": []})
    assert resposta.status_code == 401


def test_direcoes_sem_chave_configurada_responde_503(client_logado, monkeypatch):
    monkeypatch.setattr("rota_routes.ORS_API_KEY", "")
    resposta = client_logado.post("/api/rota/direcoes", json={"coordinates": [[0, 0], [1, 1]]})
    assert resposta.status_code == 503


@patch("rota_routes.requests.post")
def test_direcoes_repassa_a_resposta(mock_post, client_logado, monkeypatch):
    monkeypatch.setattr("rota_routes.ORS_API_KEY", "chave-de-teste")
    mock_post.return_value = RespostaFalsa({"routes": [{"summary": {"distance": 1200}}]})
    resposta = client_logado.post("/api/rota/direcoes", json={"coordinates": [[0, 0], [1, 1]]})
    assert resposta.status_code == 200
    assert resposta.get_json()["routes"][0]["summary"]["distance"] == 1200


@patch("rota_routes.requests.post")
def test_a_chave_vai_no_header_e_nao_no_corpo(mock_post, client_logado, monkeypatch):
    monkeypatch.setattr("rota_routes.ORS_API_KEY", "chave-de-teste")
    mock_post.return_value = RespostaFalsa({"routes": []})
    client_logado.post("/api/rota/direcoes", json={"coordinates": [[0, 0], [1, 1]]})
    _, kwargs = mock_post.call_args
    assert kwargs["headers"]["Authorization"] == "chave-de-teste"
    assert "chave-de-teste" not in str(kwargs["json"])
