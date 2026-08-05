"""
Testes de fluxo ponta a ponta que substituem a verificação manual no navegador
(Step 5 do task-3-brief.md). O Docker Desktop não está disponível nesta máquina,
então em vez de abrir a tela e testar manualmente, os mesmos cenários são
cobertos aqui via API real (cliente de testes do Django), passando pelas views
de cadastro, login e edição.
"""
import json

import pytest
from django.contrib.auth.hashers import make_password

from api.funcionarios.models import Funcionario


@pytest.mark.django_db
def test_cadastrar_funcionario_via_api_e_autenticar_depois(client):
    """Cadastra um funcionário via POST e confirma que o login com a senha
    em texto puro funciona logo em seguida (equivalente ao "cadastrar um
    funcionário novo... o login com o funcionário novo deve funcionar")."""
    resposta_cadastro = client.post(
        "/api/funcionarios/",
        data=json.dumps({
            "nome_completo": "Carlos",
            "cargo": "Eletricista",
            "email": "carlos@teste.com",
            "senha": "segredo123",
        }),
        content_type="application/json",
    )
    assert resposta_cadastro.status_code == 201, resposta_cadastro.content
    assert "senha" not in resposta_cadastro.json()

    resposta_login = client.post(
        "/api/funcionarios/login/",
        data=json.dumps({"email": "carlos@teste.com", "senha": "segredo123"}),
        content_type="application/json",
    )
    assert resposta_login.status_code == 200, resposta_login.content
    assert resposta_login.json()["success"] is True


@pytest.mark.django_db
def test_editar_sem_preencher_senha_preserva_hash_original(client):
    """Cadastra um funcionário, edita outros campos deixando a senha em branco
    e confirma que o hash original é preservado e o login antigo continua
    funcionando (equivalente a "editá-lo sem preencher a senha")."""
    funcionario = Funcionario.objects.create(
        nome_completo="Beatriz",
        cargo="Pedreira",
        email="beatriz@teste.com",
        senha=make_password("senhaoriginal"),
    )
    hash_original = funcionario.senha

    resposta_edicao = client.put(
        f"/api/funcionarios/{funcionario.id}/",
        data=json.dumps({
            "nome_completo": "Beatriz Souza",
            "cargo": "Pedreira",
            "email": "beatriz@teste.com",
            "senha": "",
        }),
        content_type="application/json",
    )
    assert resposta_edicao.status_code == 200, resposta_edicao.content

    funcionario.refresh_from_db()
    assert funcionario.nome_completo == "Beatriz Souza"
    assert funcionario.senha == hash_original

    resposta_login = client.post(
        "/api/funcionarios/login/",
        data=json.dumps({"email": "beatriz@teste.com", "senha": "senhaoriginal"}),
        content_type="application/json",
    )
    assert resposta_login.status_code == 200, resposta_login.content
    assert resposta_login.json()["success"] is True
