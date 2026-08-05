import pytest
from api.funcionarios.models import Funcionario


@pytest.mark.django_db
def test_orm_disponivel_nos_testes():
    Funcionario.objects.create(
        nome_completo="Teste", cargo="QA", email="qa@teste.com", senha="x"
    )
    assert Funcionario.objects.count() == 1
