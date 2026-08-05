import pytest
from django.contrib.auth.hashers import check_password

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
