from unittest.mock import patch

import backend_client
from config import BACKEND_URL


@patch("backend_client.requests.request")
def test_get_repassa_url_e_metodo(mock_request):
    backend_client.get("http://backend:8000/api/obras/")
    args, kwargs = mock_request.call_args
    assert args[0] == "GET"
    assert args[1] == "http://backend:8000/api/obras/"


@patch("backend_client.requests.request")
def test_patch_repassa_url_e_metodo(mock_request):
    backend_client.patch("http://backend:8000/api/ordens-servico/1/")
    args, kwargs = mock_request.call_args
    assert args[0] == "PATCH"
    assert args[1] == "http://backend:8000/api/ordens-servico/1/"


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
    monkeypatch.setattr(backend_client, "headers_extras", lambda url: {"X-Teste": "1"})
    backend_client.post("http://backend:8000/api/obras/", json={"nome": "x"})
    assert mock_request.call_args.kwargs["headers"]["X-Teste"] == "1"


@patch("backend_client.requests.request")
def test_headers_do_chamador_sao_preservados(mock_request, monkeypatch):
    monkeypatch.setattr(backend_client, "headers_extras", lambda url: {"X-Teste": "1"})
    backend_client.put("http://backend:8000/api/obras/1/", headers={"X-Outro": "2"})
    enviados = mock_request.call_args.kwargs["headers"]
    assert enviados["X-Teste"] == "1" and enviados["X-Outro"] == "2"


@patch("backend_client.requests.request")
def test_header_de_demo_so_vai_para_o_backend(mock_request, client):
    """O X-Demo-Session não pode vazar para serviços externos.

    backend_client também é usado por rota_routes.py para chamar a
    OpenRouteService (um serviço de terceiros); o id de sessão do demo não
    tem nada a ver com aquela chamada e não deve acompanhá-la.
    """
    with client.application.test_request_context("/"):
        from flask import session as sessao_flask
        sessao_flask["demo_id"] = "abc123"

        backend_client.get(f"{BACKEND_URL}/api/obras/")
        headers_backend = mock_request.call_args.kwargs.get("headers") or {}

        backend_client.post("https://api.openrouteservice.org/v2/directions/driving-car/json")
        headers_ors = mock_request.call_args.kwargs.get("headers") or {}

    assert headers_backend["X-Demo-Session"] == "abc123"
    assert "X-Demo-Session" not in headers_ors
