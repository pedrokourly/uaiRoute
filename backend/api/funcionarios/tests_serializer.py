import pytest
from django.contrib.auth.hashers import check_password, make_password

from api.funcionarios.models import Funcionario
from api.funcionarios.serializers import FuncionarioSerializer


@pytest.mark.django_db
def test_senha_nao_aparece_na_saida():
    funcionario = Funcionario.objects.create(
        nome_completo="Maria", cargo="Engenheira", email="maria@teste.com", senha="hash"
    )
    assert "senha" not in FuncionarioSerializer(funcionario).data


@pytest.mark.django_db
def test_senha_continua_sendo_gravada_criptografada():
    serializer = FuncionarioSerializer(data={
        "nome_completo": "Ana", "cargo": "Pedreira",
        "email": "ana@teste.com", "senha": "segredo123",
    })
    assert serializer.is_valid(), serializer.errors
    funcionario = serializer.save()
    assert funcionario.senha != "segredo123"
    assert check_password("segredo123", funcionario.senha)


@pytest.mark.django_db
def test_criar_sem_senha_e_rejeitado_e_nao_grava_nada():
    serializer = FuncionarioSerializer(data={
        "nome_completo": "Bruno", "cargo": "Pintor", "email": "bruno@teste.com",
    })
    assert not serializer.is_valid()
    assert "senha" in serializer.errors
    assert Funcionario.objects.count() == 0


@pytest.mark.django_db
def test_criar_com_senha_vazia_e_rejeitado_e_nao_grava_nada():
    serializer = FuncionarioSerializer(data={
        "nome_completo": "Bruno", "cargo": "Pintor", "email": "bruno@teste.com", "senha": "",
    })
    assert not serializer.is_valid()
    assert "senha" in serializer.errors
    assert Funcionario.objects.count() == 0


@pytest.mark.django_db
def test_atualizar_com_senha_vazia_preserva_hash_atual():
    funcionario = Funcionario.objects.create(
        nome_completo="Carla", cargo="Arquiteta", email="carla@teste.com",
        senha=make_password("senhaoriginal"),
    )
    hash_original = funcionario.senha

    serializer = FuncionarioSerializer(
        funcionario,
        data={
            "nome_completo": "Carla Souza", "cargo": "Arquiteta",
            "email": "carla@teste.com", "senha": "",
        },
    )
    assert serializer.is_valid(), serializer.errors
    funcionario_atualizado = serializer.save()
    assert funcionario_atualizado.senha == hash_original
