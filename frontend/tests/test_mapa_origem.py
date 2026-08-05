"""Confere que o mapa passou a usar a própria origem do Flask.

Depois que a porta 8000 deixou de ser publicada, o browser não alcança mais
o Django diretamente: o template precisa apontar para uma origem vazia
(API_BASE relativo) e não pode mais expor BACKEND_URL num <script>.
"""
from unittest.mock import patch

from requests.exceptions import ConnectionError as RequestsConnectionError


@patch("routes.requests.get", side_effect=RequestsConnectionError("backend indisponível"))
def test_mapa_renderiza_com_origem_vazia(mock_get, client_logado):
    resposta = client_logado.get("/mapa")

    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)
    assert 'const API_BASE = "";' in html
    assert "BACKEND_URL" not in html
