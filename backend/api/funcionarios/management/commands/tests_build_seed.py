import pytest
from django.core.management import call_command

from api.alojamento.models import Alojamento
from api.funcionarios.models import Funcionario
from api.obras.models import Obra
from api.ordens_servico.models import OrdemServico
from api.veiculos.models import Veiculo
from api.funcionarios.management.commands.build_seed import popular


@pytest.mark.django_db
def test_popular_cria_o_conjunto_esperado():
    popular()
    assert Alojamento.objects.count() == 3
    assert Funcionario.objects.count() == 8
    assert Obra.objects.count() == 5
    assert Veiculo.objects.count() == 4
    assert OrdemServico.objects.count() == 6


@pytest.mark.django_db
def test_tudo_que_vai_ao_mapa_tem_coordenadas():
    popular()
    for modelo in (Alojamento, Obra, Veiculo):
        assert not modelo.objects.filter(latitude__isnull=True).exists(), modelo
        assert not modelo.objects.filter(longitude__isnull=True).exists(), modelo


@pytest.mark.django_db
def test_popular_e_idempotente():
    popular()
    popular()
    assert Funcionario.objects.count() == 8


@pytest.mark.django_db
def test_as_contas_de_demonstracao_conseguem_autenticar():
    from django.contrib.auth.hashers import check_password
    popular()
    admin = Funcionario.objects.get(email="admin@teste.com")
    joao = Funcionario.objects.get(email="joao@teste.com")
    assert admin.is_admin and check_password("admin", admin.senha)
    assert not joao.is_admin and check_password("123456", joao.senha)
