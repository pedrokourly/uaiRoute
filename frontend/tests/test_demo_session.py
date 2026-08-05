from unittest.mock import patch

import pytest

import backend_client
from config import BACKEND_URL


def test_primeira_visita_cria_demo_id_e_autentica(client, backend_falso):
    client.get("/")
    with client.session_transaction() as sessao:
        assert len(sessao["demo_id"]) == 32
        assert sessao["logged_in"] is True
        assert sessao["funcionario"]["is_admin"] is True


def test_primeira_visita_a_raiz_leva_para_home(client, backend_falso):
    resposta = client.get("/")
    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/home")


def test_o_demo_id_sobrevive_ao_logout(client, backend_falso):
    client.get("/")
    with client.session_transaction() as sessao:
        id_antes = sessao["demo_id"]

    client.get("/logout")

    with client.session_transaction() as sessao:
        assert sessao["demo_id"] == id_antes
        assert not sessao.get("logged_in")


def test_nao_reautentica_quem_saiu_de_proposito(client, backend_falso):
    client.get("/")
    client.get("/logout")
    client.get("/")
    with client.session_transaction() as sessao:
        assert not sessao.get("logged_in")


@patch("backend_client.requests.request")
def test_o_header_de_demo_acompanha_as_chamadas(mock_request, client):
    client.get("/")
    with client.session_transaction() as sessao:
        id_esperado = sessao["demo_id"]

    with client.application.test_request_context("/"):
        from flask import session as sessao_flask
        sessao_flask["demo_id"] = id_esperado
        # A URL precisa apontar para o backend Django: headers_extras só
        # injeta o header de sessão nessas chamadas, nunca em serviços
        # externos como a OpenRouteService (ver backend_client.headers_extras).
        backend_client.get(f"{BACKEND_URL}/api/obras/")

    assert mock_request.call_args.kwargs["headers"]["X-Demo-Session"] == id_esperado
