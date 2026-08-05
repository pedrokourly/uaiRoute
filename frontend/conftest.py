import os
import sys

import pytest

# O app importa seus módulos por nome simples (from config import ...), então
# o diretório do frontend precisa estar no path como se fosse a raiz.
sys.path.insert(0, os.path.dirname(__file__))

from uairoute import app as flask_app  # noqa: E402


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.secret_key = "chave-de-teste"
    with flask_app.test_client() as cliente:
        yield cliente


@pytest.fixture
def client_logado(client):
    """Cliente com uma sessão de admin já estabelecida."""
    with client.session_transaction() as sessao:
        sessao["logged_in"] = True
        sessao["funcionario"] = {
            "id": 1,
            "nome_completo": "Admin Teste",
            "email": "admin@teste.com",
            "cargo": "Administrador",
            "is_admin": True,
            "alojamento": None,
        }
    return client
