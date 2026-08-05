import os
import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth.hashers import check_password
from django.conf import settings
from api.funcionarios.models import Funcionario


@pytest.mark.django_db
def test_create_admin_with_debug_true_no_password(monkeypatch):
    """
    Com DEBUG=True e sem ADMIN_PASSWORD, o comando cria o admin com fallback 'admin'.
    """
    # Limpa a variável de ambiente
    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)
    # Define DEBUG=True
    monkeypatch.setattr(settings, 'DEBUG', True)

    # Limpa qualquer admin existente
    Funcionario.objects.filter(email='admin@teste.com').delete()

    # Executa o comando
    call_command('create_admin')

    # Verifica se o admin foi criado com a senha 'admin'
    admin = Funcionario.objects.get(email='admin@teste.com')
    assert check_password('admin', admin.senha) is True
    assert admin.is_admin is True
    assert admin.nome_completo == 'Administrador'


@pytest.mark.django_db
def test_create_admin_with_debug_false_no_password(monkeypatch):
    """
    Com DEBUG=False e sem ADMIN_PASSWORD, o comando deve falhar com CommandError.
    """
    # Limpa a variável de ambiente
    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)
    # Define DEBUG=False
    monkeypatch.setattr(settings, 'DEBUG', False)

    # Limpa qualquer admin existente
    Funcionario.objects.filter(email='admin@teste.com').delete()

    # Verifica se o comando lança CommandError
    with pytest.raises(CommandError) as excinfo:
        call_command('create_admin')

    # Valida a mensagem de erro
    assert 'ADMIN_PASSWORD é obrigatória' in str(excinfo.value)


@pytest.mark.django_db
def test_create_admin_with_debug_false_with_password(monkeypatch):
    """
    Com DEBUG=False e ADMIN_PASSWORD definida, o comando cria o admin com a senha fornecida.
    """
    test_password = 'senha-super-secreta-teste'
    # Define a variável de ambiente
    monkeypatch.setenv('ADMIN_PASSWORD', test_password)
    # Define DEBUG=False
    monkeypatch.setattr(settings, 'DEBUG', False)

    # Limpa qualquer admin existente
    Funcionario.objects.filter(email='admin@teste.com').delete()

    # Executa o comando
    call_command('create_admin')

    # Verifica se o admin foi criado com a senha fornecida
    admin = Funcionario.objects.get(email='admin@teste.com')
    assert check_password(test_password, admin.senha) is True
    assert admin.is_admin is True


@pytest.mark.django_db
def test_create_admin_already_exists(monkeypatch):
    """
    Se o admin já existe, o comando apenas avisa e não cria novamente.
    """
    # Cria um admin manualmente
    Funcionario.objects.create(
        nome_completo='Admin Existente',
        cargo='Administrador',
        email='admin@teste.com',
        senha='qualquer-senha',
        is_admin=True
    )

    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)
    monkeypatch.setattr(settings, 'DEBUG', True)

    # Executa o comando (não deve criar novamente)
    call_command('create_admin')

    # Verifica se há apenas um admin
    admins = Funcionario.objects.filter(email='admin@teste.com')
    assert admins.count() == 1
    # Verifica que o nome não foi alterado
    assert admins.first().nome_completo == 'Admin Existente'
