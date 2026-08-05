from unittest.mock import patch

import backend_client


@patch("backend_client.requests.request")
def test_get_repassa_url_e_metodo(mock_request):
    backend_client.get("http://backend:8000/api/obras/")
    args, kwargs = mock_request.call_args
    assert args[0] == "GET"
    assert args[1] == "http://backend:8000/api/obras/"


@patch("backend_client.requests.request")
def test_timeout_padrao_aplicado(mock_request):
    backend_client.get("http://backend:8000/api/obras/")
    assert mock_request.call_args.kwargs["timeout"] == 15


@patch("backend_client.requests.request")
def test_timeout_explicito_prevalece(mock_request):
    backend_client.get("http://backend:8000/api/obras/", timeout=3)
    assert mock_request.call_args.kwargs["timeout"] == 3


@patch("backend_client.requests.request")
def test_headers_extras_sao_injetados(mock_request, monkeypatch):
    monkeypatch.setattr(backend_client, "headers_extras", lambda: {"X-Teste": "1"})
    backend_client.post("http://backend:8000/api/obras/", json={"nome": "x"})
    assert mock_request.call_args.kwargs["headers"]["X-Teste"] == "1"


@patch("backend_client.requests.request")
def test_headers_do_chamador_sao_preservados(mock_request, monkeypatch):
    monkeypatch.setattr(backend_client, "headers_extras", lambda: {"X-Teste": "1"})
    backend_client.put("http://backend:8000/api/obras/1/", headers={"X-Outro": "2"})
    enviados = mock_request.call_args.kwargs["headers"]
    assert enviados["X-Teste"] == "1" and enviados["X-Outro"] == "2"
