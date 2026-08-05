from unittest.mock import patch


class RespostaFalsa:
    def __init__(self, dados, status_code=200):
        self._dados = dados
        self.status_code = status_code

    def json(self):
        return self._dados


def test_proxy_exige_sessao(client):
    resposta = client.get("/api/obras")
    assert resposta.status_code == 401
    assert resposta.is_json


@patch("api_proxy_routes.requests.get")
def test_proxy_de_obras_repassa_o_json(mock_get, client_logado):
    mock_get.return_value = RespostaFalsa([{"id": 1, "nome": "Obra Centro"}])
    resposta = client_logado.get("/api/obras")
    assert resposta.status_code == 200
    assert resposta.get_json() == [{"id": 1, "nome": "Obra Centro"}]


@patch("api_proxy_routes.requests.get")
def test_proxy_de_veiculos_repassa_o_json(mock_get, client_logado):
    mock_get.return_value = RespostaFalsa([{"id": 7, "placa": "ABC1D23"}])
    assert client_logado.get("/api/veiculos").get_json() == [{"id": 7, "placa": "ABC1D23"}]


@patch("api_proxy_routes.requests.get")
def test_proxy_de_alojamentos_repassa_o_json(mock_get, client_logado):
    mock_get.return_value = RespostaFalsa([{"id": 3, "nome": "Alojamento Norte"}])
    assert client_logado.get("/api/alojamento").get_json() == [{"id": 3, "nome": "Alojamento Norte"}]


@patch("api_proxy_routes.requests.get")
def test_proxy_traduz_backend_fora_do_ar_em_502(mock_get, client_logado):
    import requests as req
    mock_get.side_effect = req.RequestException("conexão recusada")
    assert client_logado.get("/api/obras").status_code == 502
