#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def setup_admin_if_needed():
    """Verifica se o administrador existe e cria se necessário"""
    try:
        import django
        django.setup()
        
        from api.funcionarios.models import Funcionario
        from django.contrib.auth.hashers import make_password
        
        # Verifica se já existe um administrador
        if not Funcionario.objects.filter(email='admin@teste.com').exists():
            admin_user = Funcionario.objects.create(
                nome_completo='Administrador',
                cargo='Administrador',
                email='admin@teste.com',
                senha=make_password('admin'),
                is_admin=True
            )
            print("✓ Administrador padrão criado:")
            print("  Email: admin@teste.com")
            print("  Senha: admin")
    except Exception as e:
        # Se der erro (como durante migrations), ignora
        pass


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uairoute.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Se o comando for runserver, verifica e cria o admin se necessário
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        setup_admin_if_needed()
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
